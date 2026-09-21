from flask import Flask, render_template, request

from database.database import get_results, initialize_database, save_result
from modules.dns_monitor import check_dns
from modules.tcp_monitor import check_tcp
from modules.udp_monitor import check_udp
from modules.qos_monitor import measure_tcp_qos
from modules.http_monitor import check_http
from modules.smtp_monitor import check_smtp
from modules.ftp_monitor import check_ftp
from modules.snmp_monitor import check_snmp

app = Flask(__name__)
initialize_database()


def validate_port(value, default=None):
    if value in (None, ""):
        if default is None:
            raise ValueError("Port is required")
        return default
    port = int(value)
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    return port


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return {"status": "ok", "message": "SmartNet Monitor backend is running"}


@app.route("/api/dns")
def dns_check():
    hostname = request.args.get("hostname")
    if not hostname:
        return {"status": "failed", "error": "Hostname is required"}, 400
    result = check_dns(hostname)
    save_result("DNS", hostname, result["status"], result.get("response_time_ms"), details=result.get("error"))
    return result


@app.route("/api/tcp")
def tcp_check():
    host = request.args.get("host")
    if not host:
        return {"status": "failed", "error": "Host is required"}, 400
    try:
        port = validate_port(request.args.get("port"))
    except ValueError as error:
        return {"status": "failed", "error": str(error)}, 400
    result = check_tcp(host, port)
    save_result("TCP", host, result["status"], result.get("response_time_ms"), port, result.get("error"))
    return result


@app.route("/api/udp")
def udp_check():
    host = request.args.get("host")
    if not host:
        return {"status": "failed", "error": "Host is required"}, 400
    try:
        port = validate_port(request.args.get("port"))
    except ValueError as error:
        return {"status": "failed", "error": str(error)}, 400
    result = check_udp(host, port)
    save_result("UDP", host, result["status"], result.get("response_time_ms"), port, result.get("error"))
    return result


@app.route("/api/qos")
def qos_check():
    host = request.args.get("host")
    if not host:
        return {"status": "failed", "error": "Host is required"}, 400
    try:
        port = validate_port(request.args.get("port"))
        count = int(request.args.get("count", 5))
        if not 1 <= count <= 50:
            raise ValueError("Count must be between 1 and 50")
    except ValueError as error:
        return {"status": "failed", "error": str(error)}, 400

    result = measure_tcp_qos(host, port, count=count)
    qos_status = "success" if result["successful_tests"] > 0 else "failed"
    details = (
        f"Tests={result['total_tests']}; "
        f"Successful={result['successful_tests']}; "
        f"Failed={result['failed_tests']}; "
        f"Probe loss={result['packet_loss_percent']}%"
    )
    save_result("QoS", host, qos_status, result.get("average_latency_ms"), port, details)
    result["status"] = qos_status
    return result


@app.route("/api/http")
def http_check():
    url = request.args.get("url")
    if not url:
        return {"status": "failed", "error": "URL is required"}, 400
    result = check_http(url)
    save_result("HTTP", url, result["status"], result.get("response_time_ms"), details=result.get("error"))
    return result


@app.route("/api/smtp")
def smtp_check():
    host = request.args.get("host")
    if not host:
        return {"status": "failed", "error": "SMTP host is required"}, 400
    try:
        port = validate_port(request.args.get("port"), 587)
    except ValueError as error:
        return {"status": "failed", "error": str(error)}, 400
    result = check_smtp(host, port)
    save_result("SMTP", host, result["status"], result.get("response_time_ms"), port, result.get("error"))
    return result


@app.route("/api/ftp")
def ftp_check():
    host = request.args.get("host")
    if not host:
        return {"status": "failed", "error": "FTP host is required"}, 400
    try:
        port = validate_port(request.args.get("port"), 21)
    except ValueError as error:
        return {"status": "failed", "error": str(error)}, 400
    result = check_ftp(host, port)
    save_result("FTP", host, result["status"], result.get("response_time_ms"), port, result.get("error"))
    return result


@app.route("/api/snmp")
def snmp_check():
    host = request.args.get("host")
    community = request.args.get("community", "public")
    if not host:
        return {"status": "failed", "error": "SNMP host is required"}, 400
    try:
        port = validate_port(request.args.get("port"), 161)
    except ValueError as error:
        return {"status": "failed", "error": str(error)}, 400
    result = check_snmp(host, port, community)
    save_result("SNMP", host, result["status"], result.get("response_time_ms"), port, result.get("error"))
    return result


@app.route("/api/history")
def history():
    return {"status": "success", "results": get_results(100)}


@app.route("/api/summary")
def summary():
    results = get_results(1000)
    total = len(results)
    successful = sum(1 for item in results if item["status"] == "success")
    failed = total - successful
    response_times = [item["response_time_ms"] for item in results if item["response_time_ms"] is not None]
    protocol_counts = {}
    for item in results:
        protocol_counts[item["monitor_type"]] = protocol_counts.get(item["monitor_type"], 0) + 1
    availability = successful / total * 100 if total else 0
    return {
        "total": total,
        "successful": successful,
        "failed": failed,
        "availability_percent": round(availability, 2),
        "average_response_time_ms": round(sum(response_times) / len(response_times), 2) if response_times else 0,
        "protocol_counts": protocol_counts,
    }


if __name__ == "__main__":
    app.run()

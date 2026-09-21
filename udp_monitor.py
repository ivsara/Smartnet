import socket
import time


def check_udp(host, port, timeout=3):
    start_time = time.perf_counter()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.sendto(b"SmartNet Monitor UDP Test", (host, port))
            try:
                data, _ = sock.recvfrom(1024)
                response_time = (time.perf_counter() - start_time) * 1000
                return {"status": "success", "host": host, "port": port,
                        "response_received": True, "response_time_ms": round(response_time, 2),
                        "bytes_received": len(data)}
            except socket.timeout:
                response_time = (time.perf_counter() - start_time) * 1000
                return {"status": "timeout", "host": host, "port": port,
                        "response_received": False, "response_time_ms": round(response_time, 2),
                        "error": "No UDP response received"}
    except socket.gaierror:
        return {"status": "failed", "host": host, "port": port,
                "response_received": False, "error": "Hostname could not be resolved"}
    except Exception as error:
        return {"status": "failed", "host": host, "port": port,
                "response_received": False, "error": str(error)}

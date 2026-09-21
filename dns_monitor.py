import socket
import time


def check_dns(hostname):
    start_time = time.perf_counter()
    try:
        ip_address = socket.gethostbyname(hostname)
        response_time = (time.perf_counter() - start_time) * 1000
        return {"status": "success", "hostname": hostname, "ip_address": ip_address,
                "response_time_ms": round(response_time, 2)}
    except socket.gaierror:
        response_time = (time.perf_counter() - start_time) * 1000
        return {"status": "failed", "hostname": hostname, "ip_address": None,
                "response_time_ms": round(response_time, 2), "error": "DNS resolution failed"}

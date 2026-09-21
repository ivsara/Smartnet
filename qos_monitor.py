import socket
import time


def measure_tcp_qos(host, port, count=5, timeout=3):
    latencies = []
    successful = 0
    for _ in range(count):
        start_time = time.perf_counter()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
            if result == 0:
                successful += 1
                latencies.append((time.perf_counter() - start_time) * 1000)
        except Exception:
            pass
    failed = count - successful
    packet_loss = failed / count * 100
    availability = successful / count * 100
    average = sum(latencies) / len(latencies) if latencies else None
    return {
        "host": host, "port": port, "total_tests": count,
        "successful_tests": successful, "failed_tests": failed,
        "packet_loss_percent": round(packet_loss, 2),
        "availability_percent": round(availability, 2),
        "average_latency_ms": round(average, 2) if average is not None else None,
        "minimum_latency_ms": round(min(latencies), 2) if latencies else None,
        "maximum_latency_ms": round(max(latencies), 2) if latencies else None,
    }

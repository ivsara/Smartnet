import socket
import time


def check_tcp(host, port, timeout=5):
    start_time = time.perf_counter()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
        response_time = (time.perf_counter() - start_time) * 1000
        if result == 0:
            return {"status": "success", "host": host, "port": port, "connected": True,
                    "response_time_ms": round(response_time, 2)}
        return {"status": "failed", "host": host, "port": port, "connected": False,
                "response_time_ms": round(response_time, 2),
                "error": f"Connection failed with error code {result}"}
    except socket.gaierror:
        return {"status": "failed", "host": host, "port": port, "connected": False,
                "error": "Hostname could not be resolved"}
    except socket.timeout:
        return {"status": "failed", "host": host, "port": port, "connected": False,
                "error": "Connection timed out"}
    except Exception as error:
        return {"status": "failed", "host": host, "port": port, "connected": False, "error": str(error)}

import socket
import time


def check_smtp(host, port=587, timeout=5):
    start_time = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as connection:
            connection.settimeout(timeout)
            response = connection.recv(1024)
        response_time = (time.perf_counter() - start_time) * 1000
        banner = response.decode("utf-8", errors="replace").strip()
        return {"status": "success", "host": host, "port": port,
                "response_time_ms": round(response_time, 2), "banner": banner, "reachable": True}
    except socket.timeout:
        return {"status": "failed", "host": host, "port": port, "reachable": False,
                "error": "SMTP connection timed out"}
    except socket.gaierror:
        return {"status": "failed", "host": host, "port": port, "reachable": False,
                "error": "SMTP hostname could not be resolved"}
    except ConnectionRefusedError:
        return {"status": "failed", "host": host, "port": port, "reachable": False,
                "error": "SMTP connection was refused"}
    except Exception as error:
        return {"status": "failed", "host": host, "port": port, "reachable": False, "error": str(error)}

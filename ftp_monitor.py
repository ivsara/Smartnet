from ftplib import FTP
import time


def check_ftp(host, port=21, timeout=5):
    start_time = time.perf_counter()
    ftp = None
    try:
        ftp = FTP()
        ftp.connect(host=host, port=port, timeout=timeout)
        response_time = (time.perf_counter() - start_time) * 1000
        welcome_message = ftp.getwelcome()
        try:
            ftp.quit()
        except Exception:
            ftp.close()
        return {"status": "success", "host": host, "port": port,
                "response_time_ms": round(response_time, 2),
                "welcome_message": welcome_message, "reachable": True}
    except TimeoutError:
        return {"status": "failed", "host": host, "port": port, "reachable": False,
                "error": "FTP connection timed out"}
    except ConnectionRefusedError:
        return {"status": "failed", "host": host, "port": port, "reachable": False,
                "error": "FTP connection was refused"}
    except Exception as error:
        return {"status": "failed", "host": host, "port": port, "reachable": False, "error": str(error)}
    finally:
        if ftp is not None:
            try:
                ftp.close()
            except Exception:
                pass

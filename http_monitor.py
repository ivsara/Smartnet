import time
import requests


def check_http(url, timeout=10):
    start_time = time.perf_counter()
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        response_time = (time.perf_counter() - start_time) * 1000
        return {"status": "success", "url": url, "final_url": response.url,
                "status_code": response.status_code, "response_time_ms": round(response_time, 2),
                "content_size_bytes": len(response.content), "available": True}
    except requests.exceptions.Timeout:
        return {"status": "failed", "url": url, "available": False, "error": "HTTP request timed out"}
    except requests.exceptions.ConnectionError:
        return {"status": "failed", "url": url, "available": False, "error": "Could not connect to the server"}
    except requests.exceptions.RequestException as error:
        return {"status": "failed", "url": url, "available": False, "error": str(error)}
    except Exception as error:
        return {"status": "failed", "url": url, "available": False, "error": str(error)}

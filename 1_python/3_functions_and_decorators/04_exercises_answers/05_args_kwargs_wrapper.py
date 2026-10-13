"""Решение: прозрачный декоратор @log_calls."""

from functools import wraps


call_log: list[tuple[tuple, dict]] = []


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        call_log.append((args, kwargs))
        return func(*args, **kwargs)

    return wrapper


@log_calls
def add(a, b):
    return a + b


@log_calls
def build_url(host, port=80, *, secure=False, path="/"):
    scheme = "https" if secure else "http"
    return f"{scheme}://{host}:{port}{path}"


if __name__ == "__main__":
    assert add(2, 3) == 5
    assert build_url("example.com", 8080, secure=True, path="/api") == "https://example.com:8080/api"
    assert build_url("localhost") == "http://localhost:80/"

    assert call_log[0] == ((2, 3), {}), f"FAIL: {call_log[0]}"
    assert call_log[1] == (("example.com", 8080), {"secure": True, "path": "/api"}), (
        f"FAIL: {call_log[1]}"
    )
    assert call_log[2] == (("localhost",), {}), f"FAIL: {call_log[2]}"

    print("PASS")

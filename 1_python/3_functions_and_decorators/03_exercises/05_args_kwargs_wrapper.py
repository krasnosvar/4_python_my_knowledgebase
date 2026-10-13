"""Упражнение: прозрачный декоратор @log_calls, пробрасывающий любые аргументы."""


call_log: list[tuple[tuple, dict]] = []


def log_calls(func):
    # TODO: реализуйте декоратор, который перед вызовом func записывает
    # (args, kwargs) в список call_log (как кортеж (args, kwargs)),
    # а затем вызывает func с теми же аргументами и возвращает её результат.
    # Декоратор должен работать с функцией ЛЮБОЙ сигнатуры.
    raise NotImplementedError


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

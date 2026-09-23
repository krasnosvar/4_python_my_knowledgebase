"""Небольшой HTTP-сервер на чистой стандартной библиотеке (без внешних
зависимостей — специально, чтобы упражнение не требовало pip install)."""

import http.server
import socketserver

PORT = 8080


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"hello from exercise app\n")

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        # приглушаем стандартный access-лог, чтобы не засорять вывод check.sh
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"serving on {PORT}")
        httpd.serve_forever()

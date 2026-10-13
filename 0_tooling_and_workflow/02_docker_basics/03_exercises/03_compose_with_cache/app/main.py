"""HTTP-сервер на стандартной библиотеке. /health проверяет TCP-доступность
кэша по имени сервиса из docker-compose (CACHE_HOST/CACHE_PORT)."""

import http.server
import os
import socket
import socketserver

PORT = 8080
CACHE_HOST = os.environ.get("CACHE_HOST", "cache")
CACHE_PORT = int(os.environ.get("CACHE_PORT", "6379"))


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            try:
                with socket.create_connection((CACHE_HOST, CACHE_PORT), timeout=2):
                    code, body = 200, b"cache reachable\n"
            except OSError:
                code, body = 503, b"cache NOT reachable\n"
        else:
            code, body = 200, b"hello from compose exercise\n"

        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"serving on {PORT}, cache={CACHE_HOST}:{CACHE_PORT}")
        httpd.serve_forever()

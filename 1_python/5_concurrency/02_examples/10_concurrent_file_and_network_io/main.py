"""
Конкурентная работа с файлами (через executor, т.к. open()/read() блокирующие)
и сетью (через встроенный asyncio.start_server/open_connection).

Запуск: python main.py
"""
from __future__ import annotations

import asyncio
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def write_file_sync(path: Path, content: str) -> None:
    path.write_text(content)  # блокирующий вызов


def read_file_sync(path: Path) -> str:
    return path.read_text()  # блокирующий вызов


async def demo_concurrent_files() -> None:
    print("--- конкурентная работа с файлами через ThreadPoolExecutor ---")
    loop = asyncio.get_running_loop()

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        paths = [tmp_path / f"file_{i}.txt" for i in range(5)]

        with ThreadPoolExecutor(max_workers=5) as pool:
            await asyncio.gather(
                *(loop.run_in_executor(pool, write_file_sync, p, f"content-{i}")
                  for i, p in enumerate(paths))
            )
            contents = await asyncio.gather(
                *(loop.run_in_executor(pool, read_file_sync, p) for p in paths)
            )
        print(f"прочитано конкурентно: {contents}")


async def echo_server(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = await reader.read(100)
    writer.write(data.upper())
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def demo_concurrent_network() -> None:
    print("\n--- конкурентные TCP-запросы к локальному echo-серверу ---")
    server = await asyncio.start_server(echo_server, "127.0.0.1", 0)
    host, port = server.sockets[0].getsockname()

    async def client(message: str) -> str:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(message.encode())
        await writer.drain()
        writer.write_eof()
        response = await reader.read(100)
        writer.close()
        await writer.wait_closed()
        return response.decode()

    async with server:
        results = await asyncio.gather(*(client(f"msg-{i}") for i in range(5)))
    print(f"ответы сервера: {results}")


async def main() -> None:
    await demo_concurrent_files()
    await demo_concurrent_network()


if __name__ == "__main__":
    asyncio.run(main())

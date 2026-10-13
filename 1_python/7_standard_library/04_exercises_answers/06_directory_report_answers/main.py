"""Решение: 06_directory_report"""
from __future__ import annotations

import tempfile
from pathlib import Path


def build_report(root: Path) -> dict[str, tuple[int, int]]:
    stats: dict[str, list[int]] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        ext = path.suffix
        size = path.stat().st_size
        if ext not in stats:
            stats[ext] = [0, 0]
        stats[ext][0] += 1
        stats[ext][1] += size
    return {ext: (count, size) for ext, (count, size) in stats.items()}


def _make_test_tree(root: Path) -> None:
    (root / "sub").mkdir()
    (root / "a.txt").write_text("hello")
    (root / "b.txt").write_text("world!")
    (root / "sub" / "c.txt").write_text("x")
    (root / "sub" / "d.log").write_text("logline")
    (root / "no_extension").write_text("data")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_test_tree(root)
        report = build_report(root)

    assert report[".txt"][0] == 3, f"ожидали 3 .txt файла, получили {report.get('.txt')}"
    assert report[".log"][0] == 1
    assert report[""][0] == 1

    for ext, (count, size) in sorted(report.items()):
        print(f"{ext or '(без расширения)'}: {count} файлов, {size} байт")


if __name__ == "__main__":
    main()

from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from library.models import Book


class Command(BaseCommand):
    help = "Задание 2: решение через prefetch_related"

    def handle(self, *args, **options) -> None:
        with CaptureQueriesContext(connection) as ctx:
            # Исправление: prefetch_related("tags") выполняет один
            # дополнительный запрос на все теги сразу и сам сопоставляет
            # их с книгами в Python, поэтому book.tags.all() внутри цикла
            # больше не бьёт в базу.
            for book in Book.objects.prefetch_related("tags"):
                tag_names = ", ".join(tag.name for tag in book.tags.all())
                self.stdout.write(f"{book.title} -- [{tag_names}]")

        # Ожидаемый результат: 2 запроса независимо от количества книг
        # (1 на книги + 1 на все теги; до фикса было 11 запросов).
        self.stdout.write(self.style.WARNING(f"\nЗапросов выполнено: {len(ctx.captured_queries)}"))

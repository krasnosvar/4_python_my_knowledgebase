from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from library.models import Book


class Command(BaseCommand):
    help = "Задание 1: решение через select_related"

    def handle(self, *args, **options) -> None:
        with CaptureQueriesContext(connection) as ctx:
            # Исправление: select_related("author") добавляет JOIN к
            # исходному запросу, поэтому book.author.name больше не
            # тянет за собой отдельный SELECT.
            for book in Book.objects.select_related("author"):
                self.stdout.write(f"{book.title} -- {book.author.name}")

        # Ожидаемый результат: 1 запрос независимо от количества книг
        # (на тестовых данных из 02_examples было 11 запросов до фикса).
        self.stdout.write(self.style.WARNING(f"\nЗапросов выполнено: {len(ctx.captured_queries)}"))

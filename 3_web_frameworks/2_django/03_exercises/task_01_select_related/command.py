from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from library.models import Book


class Command(BaseCommand):
    help = "Задание 1: найди и исправь N+1 через select_related"

    def handle(self, *args, **options) -> None:
        with CaptureQueriesContext(connection) as ctx:
            # TODO: сейчас book.author.name на каждой итерации делает
            # отдельный SQL-запрос. Замени Book.objects.all() на вариант
            # с select_related("author"), чтобы автор подгружался одним JOIN.
            for book in Book.objects.all():
                self.stdout.write(f"{book.title} -- {book.author.name}")

        self.stdout.write(self.style.WARNING(f"\nЗапросов выполнено: {len(ctx.captured_queries)}"))

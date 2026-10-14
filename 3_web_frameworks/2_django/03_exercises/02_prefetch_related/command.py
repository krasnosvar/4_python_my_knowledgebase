from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from library.models import Book


class Command(BaseCommand):
    help = "Задание 2: найди и исправь N+1 через prefetch_related"

    def handle(self, *args, **options) -> None:
        with CaptureQueriesContext(connection) as ctx:
            # TODO: сейчас book.tags.all() на каждой итерации делает
            # отдельный SQL-запрос. Замени Book.objects.all() на вариант
            # с prefetch_related("tags") -- для ManyToMany select_related
            # не подходит.
            for book in Book.objects.all():
                tag_names = ", ".join(tag.name for tag in book.tags.all())
                self.stdout.write(f"{book.title} -- [{tag_names}]")

        self.stdout.write(self.style.WARNING(f"\nЗапросов выполнено: {len(ctx.captured_queries)}"))

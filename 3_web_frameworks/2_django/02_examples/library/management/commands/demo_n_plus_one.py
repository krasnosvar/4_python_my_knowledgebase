from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from library.models import Author, Book, Review


class Command(BaseCommand):
    help = "Показывает разницу в числе SQL-запросов до/после select_related и prefetch_related"

    def handle(self, *args, **options) -> None:
        self._seed_data()

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== select_related: Book -> Author (прямой ForeignKey) ==="))
        naive = self._count_queries(self._read_authors_naive)
        optimized = self._count_queries(self._read_authors_select_related)
        self._report("book.author.name для каждой книги", naive, optimized)

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== prefetch_related: Book -> Review (обратный ForeignKey) ==="))
        naive = self._count_queries(self._read_reviews_naive)
        optimized = self._count_queries(self._read_reviews_prefetch_related)
        self._report("book.reviews.count() для каждой книги", naive, optimized)

    # --- сидирование данных -------------------------------------------------

    def _seed_data(self) -> None:
        if Book.objects.exists():
            return

        authors = [Author.objects.create(name=f"Author {i}") for i in range(1, 6)]

        for i in range(1, 11):
            author = authors[i % len(authors)]
            book = Book.objects.create(title=f"Book {i}", author=author, published_year=2000 + i)
            for j in range(1, 4):
                Review.objects.create(
                    book=book,
                    reviewer_name=f"Reviewer {j}",
                    rating=(i + j) % 5 + 1,
                    text="Демо-отзыв для примера N+1.",
                )

        self.stdout.write(self.style.SUCCESS("Тестовые данные созданы: 5 авторов, 10 книг, по 3 отзыва на книгу."))

    # --- select_related demo -------------------------------------------------

    def _read_authors_naive(self) -> None:
        for book in Book.objects.all():
            _ = book.author.name  # каждое обращение -> отдельный SELECT к Author

    def _read_authors_select_related(self) -> None:
        for book in Book.objects.select_related("author"):
            _ = book.author.name  # автор уже подгружен через JOIN

    # --- prefetch_related demo -------------------------------------------------

    def _read_reviews_naive(self) -> None:
        for book in Book.objects.all():
            _ = book.reviews.count()  # каждое обращение -> отдельный SELECT COUNT

    def _read_reviews_prefetch_related(self) -> None:
        for book in Book.objects.prefetch_related("reviews"):
            _ = len(book.reviews.all())  # отзывы уже в памяти, доп. запросов нет

    # --- утилиты -------------------------------------------------

    def _count_queries(self, action) -> int:
        with CaptureQueriesContext(connection) as ctx:
            action()
        return len(ctx.captured_queries)

    def _report(self, label: str, naive: int, optimized: int) -> None:
        self.stdout.write(f"{label}:")
        self.stdout.write(f"  naive:     {naive} запрос(ов)")
        self.stdout.write(f"  optimized: {optimized} запрос(ов)")

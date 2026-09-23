from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    # прямой ForeignKey: у Book есть author_id -> подходит для select_related
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    published_year = models.IntegerField()
    # ManyToMany -> подходит только для prefetch_related
    tags = models.ManyToManyField(Tag, related_name="books", blank=True)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    # обратная связь book.reviews -> подходит только для prefetch_related
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    reviewer_name = models.CharField(max_length=200)
    rating = models.IntegerField()
    text = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.reviewer_name} -> {self.book_id} ({self.rating})"

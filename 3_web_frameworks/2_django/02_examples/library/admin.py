from django.contrib import admin

from .models import Author, Book, Review, Tag

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Review)

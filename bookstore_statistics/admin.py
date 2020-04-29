from django.contrib import admin
from bookstore_statistics.models import Author, Publisher, Book, Store


admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Store)

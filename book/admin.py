from django.contrib import admin

from book.models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'author_email', 'imported', 'published', 'price')


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
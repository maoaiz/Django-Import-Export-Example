from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from book.models import *


# class BookAdmin(admin.ModelAdmin):


class BookAdmin(ImportExportModelAdmin):
    list_display = ('name', 'author', 'author_email', 'imported', 'published', 'price')
    # resouce_class = BookResource

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
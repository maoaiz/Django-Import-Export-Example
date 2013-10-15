from import_export import resources
from book.models import Book


class BookResource(resources.ModelResource):

    class Meta:
        model = Book
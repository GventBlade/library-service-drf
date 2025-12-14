from rest_framework import viewsets
from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for managing books in the database."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


# Create your views here.
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializers = BookSerializer(books, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def get_book_detail(request, id):
    book = Book.objects.get(id=id)
    serializers = BookSerializer(book, many=False)
    return Response(serializers.data)

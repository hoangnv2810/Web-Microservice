from django.urls import path
from . import views

urlpatterns = [
    path('book/all', views.get_books, name="get_books"),
    path('book/<str:id>', views.get_book_detail, name="get_book_detail")
]
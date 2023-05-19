from django.urls import path
from . import views

urlpatterns = [
    path('clothes/all', views.get_clothes_all, name="get_books"),
    path('clothes/<str:id>', views.get_clothes_detail, name="get_book_detail")
]
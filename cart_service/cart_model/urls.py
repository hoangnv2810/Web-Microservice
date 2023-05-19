from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name="cart_detail"),
    path('add-cart', views.add_cart, name="add_cart"),
    path('test', views.test, name="test"),
]
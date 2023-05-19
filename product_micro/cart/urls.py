from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name="cart_detail"),
    path('add-cart', views.add_cart, name="add_cart"),
    path('remove/cart-item/<str:id>', views.remove_cart_item, name="remove_cart_item"),
]

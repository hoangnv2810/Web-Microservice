from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.checkout, name="checkout"),
    path('myorders', views.get_orders, name="myorders"),

]

from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('payment', views.payment, name='payment'),
    path('payment_return', views.payment_return, name='payment_return'),
]

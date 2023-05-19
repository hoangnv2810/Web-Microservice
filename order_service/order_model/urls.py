from django.urls import path
from . import views

urlpatterns = [
    path('/myorders', views.get_orders, name="get_orders"),
    path('/<str:id>', views.get_order, name="get_order"),
    path('', views.add_order, name="add_order"),
]
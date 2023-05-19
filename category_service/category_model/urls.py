from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.get_categories, name='categories'),
    path('category/<str:id>', views.get_category, name='category'),
    path('category/<str:name>/products', views.get_products_by_category, name='category'),
]

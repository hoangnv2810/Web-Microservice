from django.urls import path
from . import views

urlpatterns = [
    path('productId/<str:product_id>', views.create_rating, name='create_rating'),
    # path('<int:pk>/', views.get_rating, name='get_rating'),
]

from django.urls import path
from . import views

urlpatterns = [

    path('login', views.MyTokenObtainPairView.as_view(), name='login'),
    path('register', views.register_user, name='register'),
    path('authenticate', views.authenticate_user.as_view(), name='authenticate'),

]
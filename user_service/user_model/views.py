from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from user_model.serializers import UserSerializerWithToken

# Create your views here.

from django.http import JsonResponse
from django.contrib.auth import authenticate, login


class authenticate_user(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            print("username: " + username)
            return Response({"username": username}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('Tài khoản hoặc mật khẩu không chính xác!')
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)

        return Response(serializer.data)

    except:
        message = {'detail': 'Tên đăng nhập đã được sử dụng!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

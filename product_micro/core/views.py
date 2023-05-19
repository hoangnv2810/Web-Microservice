from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Category, Product
from core.serializers import ProductSerializer, CategorySerializer, UserSerializerWithToken


# Create your views here.
@api_view(['GET'])
def getProductByCategory(request, id):
    if id != None:
        categories = get_object_or_404(Category, id=id)
        products = Product.objects.filter(category=categories)
    else:
        products = Product.objects.all()
    serializers = ProductSerializer(products, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def getCategory(request, id):
    category = Category.objects.get(id=id)
    serializers = CategorySerializer(category, many=False)
    return Response(serializers.data)


@api_view(['GET'])
def getCategoryList(request):
    category = Category.objects.all()
    serializers = CategorySerializer(category, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializers = ProductSerializer(products, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def getProduct_Detail(request, id):
    product = Product.objects.get(id=id)
    serializers = ProductSerializer(product, many=False)
    return Response(serializers.data)


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
def registerUser(request):
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

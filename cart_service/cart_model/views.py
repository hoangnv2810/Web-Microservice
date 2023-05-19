import json

from django.shortcuts import render
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

from .models import cart as Cart, cart_item as CartItem
from .serializers import CartSerializer, AddToCartSerializer


# Create your views here.
@api_view(['GET'])
def cart_detail(request):
    token = request.headers.get('Authorization')
    print("Token:" + token)
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.get("http://127.0.0.1:8000/api/authenticate", headers=headers)
    if response.status_code == 200:
        data = response.json()
        username = data['username']
        try:
            cart = Cart.objects.get(username=username)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(username=username)
        cart_items = CartItem.objects.filter(cart=cart)
        if len(cart_items) == 0:
            return Response({'detail': 'Không có sản phẩm nào trong giỏ hàng'})
        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data)
    else:
        return Response(response.json())


@api_view(['GET'])
def test(request):
    token = request.headers.get('Authorization')
    print("Token:" + token)
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.get("http://127.0.0.1:8000/api/authenticate", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return Response({'message': 'Xác thực thành công', 'username': data['username']}, status=status.HTTP_200_OK)
    else:
        return Response(response.json())


@api_view(['POST'])
def add_cart(request):
    token = request.headers.get('Authorization')
    print("Token:" + token)
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.get("http://127.0.0.1:8000/api/authenticate", headers=headers)
    if response.status_code == 200:
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            category = serializer.validated_data['category']
            data = response.json()
            username = data['username']

            try:
                cart = Cart.objects.get(username=username)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(username=username)

            try:
                cart_item = CartItem.objects.get(cart_id=cart.id, product_id=product_id, category=category)
                cart_item.quantity += quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                CartItem.objects.create(cart=cart, product_id=product_id, quantity=quantity, category=category)

            if category == "clothes":
                port = 8087
            else:
                port = 8086

            url = f'http://127.0.0.1:{port}/{category}/{product_id}'
            response = requests.get(url)
            product = response.json()
            cart.total_item += quantity
            cart.total_price += float(product['price']) * quantity
            cart.save()

            return Response({"message": "Sản phẩm đã được thêm vào giỏ hàng."}, status=200)
        else:
            return Response({'detail': 'Lỗi'}, status=400)
    else:
        return Response(response.json())



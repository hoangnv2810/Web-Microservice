import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
import requests


# Create your views here.
@api_view(['GET'])
def get_orders(request):
    token = request.headers.get('Authorization')
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.get("http://127.0.0.1:8000/api/authenticate", headers=headers)
    if response.status_code == 200:
        data = response.json()
        username = data['username']
        orders = Order.objects.filter(username=username)
        if len(orders) == 0:
            return Response({'detail': 'Bạn không có đơn hàng nào'})
        else:
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
    else:
        return Response(response.json())


@api_view(['GET'])
def get_order(request, id):
    token = request.headers.get('Authorization')
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.get("http://127.0.0.1:8000/api/authenticate", headers=headers)
    if response.status_code == 200:
        try:
            orders = Order.objects.get(id=id)
            serializer = OrderSerializer(orders, many=False)
            return Response(serializer.data)
        except:
            return Response({"message": "Đơn hàng không tồn tại"}, status=404)
    else:
        return Response({"message": "Bạn không có quyền truy cập"}, status=401)


@api_view(['POST'])
def add_order(request):
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
        cart = requests.get('http://127.0.0.1:8084/api/cart', headers=headers).json()
        ord = Order.objects.create(
            username=username,
            number_phone=request.data['number_phone'],
            address=request.data['address'],
            total_price=56000,
            note=request.data['note'],
        )

        for i in cart['cart_items']:
            item = OrderItem.objects.create(
                product_id=i['product_id'],
                category=i['category'],
                quantity=i['quantity'],
                sub_price=123,
                order=ord
            )

        url = "http://127.0.0.1:8088/payment"

        payload = json.dumps({
            "order_id": ord.id,
            "amount": ord.total_price,
            "order_desc": ord.note,
            "bank_code": "ncb",
            "language": "vn"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            ord.is_paid = True
            ord.save()
            return Response(response.json())
        except:
            return Response({"message": "Lỗi"})
    else:
        return Response(response.json())

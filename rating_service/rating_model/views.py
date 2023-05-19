import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rating_model.models import Rating
from rating_model.serializers import RatingSerializer


# Create your views here.

@api_view(['POST'])
def create_rating(request, product_id):
    try:
        order_id = request.data['order_id']
        token = request.headers.get('Authorization')
        url = f"http://127.0.0.1:8085/api/order/{order_id}"
        headers = {
            'Authorization': token
        }
        try:
            response = requests.request("GET", url, headers=headers)
        except:
            return Response(response.json(), status=401)
        data = response.json()
        order_items = data['order_items']
        if check_product_id_in_order_items(order_items, product_id):
            rating = Rating.objects.create(
                username=data['username'],
                order_id=order_id,
                product_id=product_id,
                category=get_category(order_items, product_id),
                rating=request.data['rating'],
                comment=request.data['comment'],
            )
            serializer = RatingSerializer(rating, many=False)
            return Response(serializer.data)
        else:
            return Response({"message": "Sản phẩm này không có trong đơn hàng"}, status=401)
    except:
        return Response({"message": "Lỗi xác thực hoặc bạn không có quyền truy cập "}, status=401)


def check_product_id_in_order_items(order_items, product_id):
    for item in order_items:
        if item['product_id'] == product_id:
            return True
    return False


def get_category(order_items, product_id):
    for item in order_items:
        if item['product_id'] == product_id:
            return item['category']

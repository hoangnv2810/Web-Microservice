from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, AddToCartSerializer
from core.models import Product


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    user_id = request.user
    try:
        cart = Cart.objects.get(user_id=user_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user_id=user_id)
    cart_items = CartItem.objects.filter(cart=cart)
    if len(cart_items) == 0:
        return Response({'detail': 'Không có sản phẩm nào trong giỏ hàng'})
    serializer = CartSerializer(cart, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        user_id = request.user.id

        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user_id=user_id)

        try:
            cart_item = CartItem.objects.get(cart_id=cart.id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product_id=product_id, quantity=quantity)

        cart.total_item += quantity
        cart.total_price += cart_item.product.price * quantity
        cart.save()

        return Response({"message": "Sản phẩm đã được thêm vào giỏ hàng."}, status=200)
    else:
        return Response({'detail': 'Lỗi'}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, id):
    user_id = request.user.id
    try:
        cart_item = CartItem.objects.get(id=id, cart__user_id=user_id)
    except CartItem.DoesNotExist:
        return Response({"message": "CartItem không tồn tại"}, status=400)

    cart = cart_item.cart
    cart.total_item -= cart_item.quantity
    cart.total_price -= cart_item.product.price * cart_item.quantity

    cart_item.delete()
    cart.save()

    return Response({"message": "Xóa thành công"}, status=200)

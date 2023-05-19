from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart, CartItem
from checkout.models import Order, OrderItem
from core.models import Product
from checkout.serializers import OrderSerializer


# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    orders = user.order_set.all()
    if len(orders) == 0:
        return Response({'detail': 'Bạn không có đơn hàng nào'})
    else:
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    cart = Cart.objects.get(user_id=request.user.id)
    try:
        cart_items = cart.cartitem_set.all()
    except CartItem.DoesNotExist:
        return Response({'detail': 'Không có ản phẩm nào'}, status=400)

    if cart_items and len(cart_items) == 0:
        return Response({'detail': 'Không có sản phẩm vui lòng thử lại'}, status=400)
    else:
        order = Order.objects.create(
            user=request.user,
            number_phone=request.data['number_phone'],
            address=request.data['address'],
            total_price=cart.total_price,
            note=request.data['note'],
        )

        for i in cart_items:
            product = i.product

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.product_name,
                quantity=i.quantity,
                price=i.product.price,
                image="http://127.0.0.1:8000" + product.images.url,
            )

            product.stock -= item.quantity
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


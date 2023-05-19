from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Product
from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def get_cart_items(self, obj):
        items = CartItem.objects.filter(cart=obj).prefetch_related('product')
        serializer = CartItemSerializer(items, many=True)
        return serializer.data


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def validate(self, data):
        try:
            Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError("Sản phẩm không tồn tại")

        return data

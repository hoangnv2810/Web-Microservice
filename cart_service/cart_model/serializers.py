from django.contrib.auth.models import User
from rest_framework import serializers
from .models import cart, cart_item


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = cart
        fields = '__all__'

    def get_cart_items(self, obj):
        items = obj.cart_item_set.all()
        serializer = CartItemSerializer(items, many=True)
        return serializer.data


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_item
        fields = '__all__'


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)


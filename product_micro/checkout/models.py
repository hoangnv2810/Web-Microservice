from django.contrib.auth.models import User
from django.db import models

from cart.models import Cart
from core.models import Product


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    number_phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    note = models.TextField(max_length=200, null=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.user}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    image = models.URLField(max_length=200)

    def __str__(self):
        return str(self.order)

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from core.models import Product


# Create your models here.
class Cart(models.Model):
    total_price = models.FloatField(default=0)
    total_item = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Cart ID {self.id} for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Quantity {self.quantity} of {self.product.product_name} in cart {self.cart.id}"

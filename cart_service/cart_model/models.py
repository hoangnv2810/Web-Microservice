from django.db import models


# Create your models here.
class cart(models.Model):
    username = models.CharField(max_length=100)
    total_price = models.FloatField(default=0)
    total_item = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class cart_item(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.SET_NULL, null=True)
    product_id = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(f"{self.id} of cart {self.cart.username}")

from django.db import models


# Create your models here.
class Order(models.Model):
    username = models.CharField(max_length=20)
    number_phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    note = models.TextField(max_length=200, null=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    # is_delivered = models.BooleanField(default=False)
    # delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order id {self.id} of {self.username}"


class OrderItem(models.Model):
    product_id = models.CharField(max_length=20, null=False)
    category = models.CharField(max_length=20, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    sub_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return str(self.order)

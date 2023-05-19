from django.db import models
from django.contrib.auth.models import User


class Rating(models.Model):
    username = models.CharField(max_length=100, null=False)
    order_id = models.IntegerField()
    product_id = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('username', 'order_id')

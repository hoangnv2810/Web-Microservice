from django.db import models


# Create your models here.
class Clothes(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/clothes")
    categories = models.CharField(max_length=200)
    availability = models.CharField(max_length=15)
    price = models.CharField(max_length=10)

    def __str__(self):
        return self.name


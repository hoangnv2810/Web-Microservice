from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    description = models.TextField()
    image = models.ImageField(max_length=255, upload_to='images/products/books')
    genre = models.CharField(max_length=200)
    availability = models.CharField(max_length=15)
    price = models.CharField(max_length=10)

    def __str__(self):
        return self.title

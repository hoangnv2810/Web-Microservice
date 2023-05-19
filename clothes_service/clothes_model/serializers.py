from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Clothes


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'

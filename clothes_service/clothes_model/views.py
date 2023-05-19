from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Clothes
from .serializers import ClothesSerializer


# Create your views here.
@api_view(['GET'])
def get_clothes_all(request):
    books = Clothes.objects.all()
    serializers = ClothesSerializer(books, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def get_clothes_detail(request, id):
    clothes = Clothes.objects.get(id=id)
    serializers = ClothesSerializer(clothes, many=False)
    return Response(serializers.data)

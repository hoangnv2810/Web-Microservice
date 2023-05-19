import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from .models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def get_category(request, id):
    category = Category.objects.get(id=id)
    serializers = CategorySerializer(category, many=False)
    return Response(serializers.data)


@api_view(['GET'])
def get_categories(request):
    category = Category.objects.all()
    serializers = CategorySerializer(category, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def get_products_by_category(request, name):
    try:
        if name == "books":
            port = 8086
        else:
            port = 8087
        response = requests.request("GET", f"http://127.0.0.1:{port}/{name}/all")
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data, content_type='application/json', safe=False)
    except requests.exceptions.RequestException as e:
        return HttpResponseServerError(f"Error connecting to the server: {e}")
    except json.JSONDecodeError as e:
        return HttpResponseServerError(f"Error decoding JSON response: {e}")

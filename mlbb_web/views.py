import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


DEPRECATION_MESSAGE = (
    "This website is no longer maintained as no one supports the project. "
    "If you'd like to continue it, please sponsor me on GitHub Sponsors. "
    "Thanks for using this project!"
)

# Create your views here.
@api_view(['GET'])
def simple_view(request):
    data = {
        "code": 200,
        "status": "success",
        "message": DEPRECATION_MESSAGE,
        "data": {
            "support me": "https://github.com/sponsors/ridwaanhall",
            "website": "https://ridwaanhall.com",
        }
    }
    return Response(data)

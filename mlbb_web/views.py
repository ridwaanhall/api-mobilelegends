from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def simple_view(request):
    data = {
        "code": 200,
        "status": "ok",
        "message": "Hello ridwaanhall"
    }
    return JsonResponse(data)
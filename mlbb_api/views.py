from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

# Create your views here.
@api_view(['GET'])
def DocsByRidwaanhall(request):
    return Response(
        {
            "code": 200,
            "status": "success",
            "message": "This website is no longer maintained as no one supports the project. If you'd like to continue it, please sponsor me on GitHub Sponsors. Thanks for using this project!",
            "data": {
                "api_docs": "https://mlbb-stats-docs.ridwaanhall.com/",
                "message": "Please visit api_docs for how can you set the API"
            }
        }
    )

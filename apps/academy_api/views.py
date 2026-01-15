from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests
from typing import Any, Dict
from apps.academy_api.utils import BasePathProvider


from django.conf import settings

MLBB_URL = settings.MLBB_URL

class APIAvailabilityMixin:
    """Mixin to check API availability for class-based views."""
    def dispatch(self, request, *args, **kwargs):
        if not settings.IS_AVAILABLE:
            status_info = settings.API_STATUS_MESSAGES['limited']
            return Response({
                'error': 'Service Unavailable',
                'status': status_info['status'],
                'message': status_info['message'],
                'available_endpoints': status_info['available_endpoints']
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return super().dispatch(request, *args, **kwargs)

# Create your views here.
class MLBBHeaderBuilder:
    @staticmethod
    def get_lang_header(lang: str) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if lang and lang != 'en':
            headers['x-lang'] = lang
        return headers


class ErrorResponseMixin:
    @staticmethod
    def error_response(message: str, details: Any = None, status_code: int = 400) -> Response:
        return Response({'error': message, 'details': details}, status=status_code)
    

class HeroView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path_academy()
        url_hero = f"{MLBB_URL}{base_path}/2766683"

        lang = request.GET.get('lang', 'en')

        payload = {
            "pageSize": 200,
            "pageIndex": 1,
            "filters": [],
            "sorts": [],
            "fields": [
                "head",
                "head_big",
                "hero.data.name",
                "hero.data.roadsort",
                "hero_id",
                "painting"
            ],
            "object": [2667538]
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_hero, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)
    
    
class EquipmentView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path_academy()
        url_equipment = f"{MLBB_URL}{base_path}/2713995"

        lang = request.GET.get('lang', 'en')
        # page = int(request.GET.get('page', 1))

        payload = {
            "pageSize":200,
            "pageIndex": 1,
            "filters":[],
            "sorts":[]
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_equipment, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)
    
    
class VersionView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path_academy()
        url_version = f"{MLBB_URL}{base_path}/2718124"

        lang = request.GET.get('lang', 'en')
        
        payload = {
            "pageSize": 20,
            "pageIndex": 1,
            "filters": [
                {
                    "field": "formId",
                    "operator": "eq",
                    "value": 2777742
                }
            ],
            "sorts": [
                {
                    "data": {
                        "field": "createdAt",
                        "order": "desc"
                    },
                    "type": "sequence"
                }
            ],
            "type": "form.item.all",
            "object": [2675413]
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_version, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)
    
    
class RecommendedView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path_academy()
        url_version = f"{MLBB_URL}{base_path}/2718124"

        lang = request.GET.get('lang', 'en')
        page = int(request.GET.get('page', 1))
        
        payload = {
            "pageSize": 10,
            "pageIndex": page,
            "filters": [
                {
                    "field": "formId",
                    "operator": "eq",
                    "value": 2737553
                },
                {
                    "field": "data.state",
                    "operator": "eq",
                    "value": "release"
                },
                {
                    "field": "data.channels",
                    "operator": "in",
                    "value": ["recommend"]
                },
                {
                    "field": "uin",
                    "operator": "contain",
                    "value": "/.*/"
                },
                {
                    "field": "data.data.game_version",
                    "operator": "contain",
                    "value": "/.*/"
                },
                {
                    "field": "data.data.language",
                    "operator": "eq",
                    "value": lang
                },
                {
                    "field": "createdAt",
                    "operator": "gte",
                    "value": 1
                }
            ],
            "sorts": [
                {
                    "data": {
                        "field": "dynamic.hot",
                        "order": "desc"
                    },
                    "type": "sequence"
                },
                {
                    "data": {
                        "field": "createdAt",
                        "order": "desc"
                    },
                    "type": "sequence"
                }
            ],
            "type": "form.item.all",
            "object": [2675413]
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_version, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)
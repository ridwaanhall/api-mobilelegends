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
    
    
class RecommendedDetailView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, recommended_id):
        base_path = BasePathProvider.get_base_path_academy()
        url_version = f"{MLBB_URL}{base_path}/2718124"

        lang = request.GET.get('lang', 'en')

        if not recommended_id:
            return self.error_response('Missing recommended id', status_code=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            "pageSize": 20,
            "pageIndex": 1,
            "filters": [
                {
                    "field": "formId",
                    "operator": "eq",
                    "value": 2737553
                },
                {
                    "field": "id",
                    "operator": "eq",
                    "value": recommended_id
                },
                {
                    "field": "data.state",
                    "operator": "eq",
                    "value": "release"
                }
            ],
            "sorts": [],
            "type": "form.item.all",
            "object": [2675413]
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_version, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)


class GuideView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    '''
    Docstring for GuideView
    This similar to hero list but get filtered by roles and lanes.
    '''
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path_academy()
        url_guide = f"{MLBB_URL}{base_path}/2766683"

        lang = request.GET.get('lang', 'en')
        
        size = request.GET.get('size', 2000)
        page = request.GET.get('page', 1)

        payload = {
            "pageSize": size,
            "pageIndex": page,
            "filters": [
                {
                    "field": "<hero.data.sortid>",
                    "operator": "hasAnyOf",
                    "value": [1, 2, 3, 4, 5, 6] # 1 = Tank (t), 2 = Fighter (f), 3 = Assassin (a), 4 = Mage (m), 5 = Marksman (mm), 6 = Support (s)
                },
                {
                    "field": "<hero.data.roadsort>",
                    "operator": "hasAnyOf",
                    "value": [1, 2, 3, 4, 5] # 1 = EXP (e), 2 =  Mid (m), 3 = Roam (r), 4 = Jungle (j), 5 = Gold (g)
                }
            ],
            "sorts": [
                {
                    "data": {
                        "field": "hero_id",
                        "order": "desc"
                    },
                    "type": "sequence"
                }
            ],
            "fields": ["head", "hero_id", "hero.data.name"],
            "object": []
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_guide, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)
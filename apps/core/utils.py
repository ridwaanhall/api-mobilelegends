from functools import wraps
from typing import Any, Dict

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


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


def web_availability_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not settings.IS_AVAILABLE:
            status_info = settings.API_STATUS_MESSAGES['limited']
            return JsonResponse({
                'error': 'Service Unavailable',
                'status': status_info['status'],
                'message': status_info['message'],
                'available_endpoints': ['Home page only']
            }, status=503)
        return view_func(request, *args, **kwargs)

    return wrapper

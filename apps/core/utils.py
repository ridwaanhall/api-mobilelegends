from functools import wraps
from typing import Any, Dict
import random

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
                'status': 'error',
                'code': 'SERVICE_UNAVAILABLE',
                'message': status_info['message'],
                'available_endpoints': status_info['available_endpoints'],
                'support': {
                    'livechat': ErrorResponseMixin.LIVECHAT_LINK,
                    'contact': ErrorResponseMixin.CONTACT_FORM_LINK,
                }
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        parent = super()
        return parent.dispatch(request, *args, **kwargs)  # type: ignore[attr-defined]


class MLBBHeaderBuilder:
    USER_AGENTS = [
        # Android phones
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",

        # iPhones
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",

        # iPads
        "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",

        # Windows desktops
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/143.0.0.0 Safari/537.36",

        # macOS desktops
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",

        # Linux desktops
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    ]

    @classmethod
    def get_random_user_agent(cls) -> str:
        return random.choice(cls.USER_AGENTS)

    @staticmethod
    def get_lang_header(lang: str) -> Dict[str, str]:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': MLBBHeaderBuilder.get_random_user_agent(),
        }
        if lang and lang != 'en':
            headers['x-lang'] = lang
        return headers


class ErrorResponseMixin:
    LIVECHAT_LINK = 'https://ridwaanhall.com/guestbook/'
    CONTACT_FORM_LINK = 'https://ridwaanhall.com/contact/'

    @classmethod
    def _build_error_code(cls, status_code: int, message: str) -> str:
        message_normalized = (message or '').lower()
        if 'failed to fetch data' in message_normalized:
            return 'UPSTREAM_REQUEST_FAILED'
        if status_code == 400:
            return 'BAD_REQUEST'
        if status_code == 404:
            return 'RESOURCE_NOT_FOUND'
        if status_code == 429:
            return 'TOO_MANY_REQUESTS'
        if status_code >= 500:
            return 'INTERNAL_SERVER_ERROR'
        return 'REQUEST_FAILED'

    @classmethod
    def _build_error_message(cls, status_code: int, message: str) -> str:
        message_normalized = (message or '').lower()
        if 'failed to fetch data' in message_normalized:
            return 'We could not process your request right now due to an upstream service issue. Please contact support.'
        if status_code >= 500:
            return 'An internal server error occurred. Please contact support.'
        return message or 'Request failed.'

    @staticmethod
    def error_response(message: str, details: Any = None, status_code: int = 400) -> Response:
        safe_payload = {
            'status': 'error',
            'code': ErrorResponseMixin._build_error_code(status_code, message),
            'message': ErrorResponseMixin._build_error_message(status_code, message),
            'support': {
                'livechat': ErrorResponseMixin.LIVECHAT_LINK,
                'contact': ErrorResponseMixin.CONTACT_FORM_LINK,
            }
        }

        # Never expose raw upstream response text to clients.
        message_normalized = (message or '').lower()
        if 'failed to fetch data' not in message_normalized and details is not None:
            safe_payload['details'] = details

        return Response(safe_payload, status=status_code)


def web_availability_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not settings.IS_AVAILABLE:
            status_info = settings.API_STATUS_MESSAGES['limited']
            return JsonResponse({
                'status': 'error',
                'code': 'SERVICE_UNAVAILABLE',
                'message': status_info['message'],
                'available_endpoints': ['Home page only'],
                'support': {
                    'livechat': ErrorResponseMixin.LIVECHAT_LINK,
                    'contact': ErrorResponseMixin.CONTACT_FORM_LINK,
                }
            }, status=503)
        return view_func(request, *args, **kwargs)

    return wrapper

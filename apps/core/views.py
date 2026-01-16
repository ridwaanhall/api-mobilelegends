from typing import Dict

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def _get_other_mlbb_api_endpoints(request) -> Dict[str, str]:
    """Return new MLBB API endpoints based on API availability."""
    base_url = request.build_absolute_uri('/api/')
    if settings.IS_AVAILABLE:
        return {
            'win_rate': f'{base_url}win-rate/?match-now=100&wr-now=50&wr-future=75',
        }
    return {}


def _get_new_mpl_id_endpoints(request) -> Dict[str, str]:
    """Return new MPL ID endpoints based on API availability."""
    base_url = request.build_absolute_uri('/api/mplid/')
    if settings.IS_AVAILABLE:
        return {
            'standings': f'{base_url}standings/',
            'teams': f'{base_url}teams/',
            'team_detail': f'{base_url}teams/{{team_id}}/',
            'transfers': f'{base_url}transfers/',
            'team_stats': f'{base_url}team-stats/',
            'player_stats': f'{base_url}player-stats/',
            'hero_stats': f'{base_url}hero-stats/',
            'hero_pools': f'{base_url}hero-pools/',
            'player_pools': f'{base_url}player-pools/',
            'standings_mvp': f'{base_url}standings-mvp/',
            'schedule': f'{base_url}schedule/',
            'schedule_week': f'{base_url}schedule/week/{{week_number}}/',
            'schedule_all_weeks': f'{base_url}schedule/week/',
        }
    return {}


def _get_mlbb_stats_endpoints(request) -> Dict[str, str]:
    """Return available endpoints based on API availability."""
    base_url = request.build_absolute_uri('/api/')
    if settings.IS_AVAILABLE:
        return {
            'documentation': f'{base_url}',
            'hero_list': f'{base_url}hero-list/',
            'hero_rank': f'{base_url}hero-rank/',
            'hero_position': f'{base_url}hero-position/',
            'hero_detail': f'{base_url}hero-detail/{{hero_id_or_name}}/',
            'hero_detail_stats': f'{base_url}hero-detail-stats/{{hero_id_or_name}}/',
            'hero_skill_combo': f'{base_url}hero-skill-combo/{{hero_id_or_name}}/',
            'hero_rate': f'{base_url}hero-rate/{{hero_id_or_name}}/',
            'hero_relation': f'{base_url}hero-relation/{{hero_id_or_name}}/',
            'hero_counter': f'{base_url}hero-counter/{{hero_id_or_name}}/',
            'hero_compatibility': f'{base_url}hero-compatibility/{{hero_id_or_name}}/'
        }
    return {'documentation': f'{base_url}'}


class MlbbApiEndpoints(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        status_info = settings.API_STATUS_MESSAGES['available'] if settings.IS_AVAILABLE else settings.API_STATUS_MESSAGES['limited']
        return Response({
            "code": 200,
            "status": "success",
            "message": "Request processed successfully",
            "meta": {
                "version": settings.API_VERSION,
                "author": "ridwaanhall",
                "support": {
                    "status": status_info['status'],
                    "message": status_info['message'],
                    "support_message": settings.SUPPORT_DETAILS['support_message'],
                    "github_sponsors": settings.SUPPORT_DETAILS['github_sponsors'],
                    "buymeacoffee": settings.SUPPORT_DETAILS['buymeacoffee'],
                },
                "available_endpoints": status_info['available_endpoints']
            },
            "services": {
                "mlbb_api": {
                    "status": status_info['status'],
                    "message": "MLBB API is currently under maintenance." if not settings.IS_AVAILABLE else "MLBB API is online.",
                    "endpoints": _get_mlbb_stats_endpoints(request)
                },
                "mpl_id": {
                    "status": status_info['status'],
                    "message": "MPL ID API is currently under maintenance." if not settings.IS_AVAILABLE else "MPL ID API is online.",
                    "endpoints": _get_new_mpl_id_endpoints(request)
                },
                "other_mlbb_api": {
                    "status": status_info['status'],
                    "message": "MLBB new API is currently under maintenance." if not settings.IS_AVAILABLE else "MLBB API is online.",
                    "endpoints": _get_other_mlbb_api_endpoints(request)
                },
            },
            "links": {
                "api_url": "https://mlbb-stats.ridwaanhall.com/api/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
                "web_url": "https://mlbb-stats.ridwaanhall.com/hero-rank/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
                "docs": "https://mlbb-stats-docs.ridwaanhall.com/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            }
        }, status=status.HTTP_200_OK)

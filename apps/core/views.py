from typing import Dict

from django.utils import timezone

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def _get_other_mlbb_api_endpoints(request) -> Dict[str, str]:
    """Return new MLBB API endpoints based on API availability."""
    if settings.IS_AVAILABLE:
        return {
            'win_rate': '/api/win-rate/?match-now=100&wr-now=50&wr-future=75',
        }
    return {}


def _get_new_mpl_id_endpoints(request) -> Dict[str, str]:
    """Return new MPL ID endpoints based on API availability."""
    if settings.IS_AVAILABLE:
        return {
            'standings': '/api/mplid/standings/',
            'teams': '/api/mplid/teams/',
            'team_detail': '/api/mplid/teams/{team_id}/',
            'transfers': '/api/mplid/transfers/',
            'team_stats': '/api/mplid/team-stats/',
            'player_stats': '/api/mplid/player-stats/',
            'hero_stats': '/api/mplid/hero-stats/',
            'hero_pools': '/api/mplid/hero-pools/',
            'player_pools': '/api/mplid/player-pools/',
            'standings_mvp': '/api/mplid/standings-mvp/',
            'schedule': '/api/mplid/schedule/',
            'schedule_week': '/api/mplid/schedule/week/{week_number}/',
            'schedule_all_weeks': '/api/mplid/schedule/week/',
        }
    return {}


def _get_mlbb_stats_endpoints(request) -> Dict[str, str]:
    """Return available endpoints based on API availability."""
    if settings.IS_AVAILABLE:
        return {
            'documentation': '/api/',
            'hero_list': '/api/hero-list/',
            'hero_rank': '/api/hero-rank/',
            'hero_position': '/api/hero-position/',
            'hero_detail': '/api/hero-detail/{hero_id_or_name}/',
            'hero_detail_stats': '/api/hero-detail-stats/{hero_id_or_name}/',
            'hero_skill_combo': '/api/hero-skill-combo/{hero_id_or_name}/',
            'hero_rate': '/api/hero-rate/{hero_id_or_name}/',
            'hero_relation': '/api/hero-relation/{hero_id_or_name}/',
            'hero_counter': '/api/hero-counter/{hero_id_or_name}/',
            'hero_compatibility': '/api/hero-compatibility/{hero_id_or_name}/'
        }
    return {'documentation': '/api/'}


def _get_mlbb_academy_endpoints(request) -> Dict[str, str]:
    """Return MLBB Academy endpoints based on API availability."""
    if settings.IS_AVAILABLE:
        return {
            'version': '/api/academy/version/',
            'heroes': '/api/academy/heroes/',
            'roles': '/api/academy/roles/',
            'equipment': '/api/academy/equipment/',
            'equipment_details': '/api/academy/equipment-details/',
            'spells': '/api/academy/spells/',
            'emblems': '/api/academy/emblems/',
            'recommended': '/api/academy/recommended/',
            'recommended_detail': '/api/academy/recommended/{recommended_id}/',
            'guide': '/api/academy/guide/',
            'guide_stats': '/api/academy/guide/{hero_id}/stats/',
            'guide_lane': '/api/academy/guide/{hero_id}/lane/',
            'guide_time_win_rate': '/api/academy/guide/{hero_id}/time-win-rate/{lane_id}/',
            'guide_builds': '/api/academy/guide/{hero_id}/builds/',
            'guide_counters': '/api/academy/guide/{hero_id}/counters/',
            'guide_teammates': '/api/academy/guide/{hero_id}/teammates/',
            'guide_trends': '/api/academy/guide/{hero_id}/trends/',
            'guide_recommended': '/api/academy/guide/{hero_id}/recommended/',
            'hero_ratings': '/api/academy/hero-ratings/',
            'hero_ratings_subject': '/api/academy/hero-ratings/{subject}/',
        }
    return {}


class MlbbApiEndpoints(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        status_info = settings.API_STATUS_MESSAGES['available'] if settings.IS_AVAILABLE else settings.API_STATUS_MESSAGES['limited']
        status_key = 'available' if settings.IS_AVAILABLE else 'limited'
        timestamp = timezone.now().astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
        base_api_url = settings.API_BASE_URL.rstrip('/') + '/'
        base_web_url = settings.WEB_BASE_URL.rstrip('/') + '/'
        base_docs_url = settings.DOCS_BASE_URL.rstrip('/') + '/'
        return Response({
            "code": 200,
            "status": "success",
            "message": "Request processed successfully",
            "timestamp": timestamp,
            "meta": {
                "version": settings.API_VERSION,
                "author": "ridwaanhall",
                "base_url": base_api_url,
                "support": {
                    "status": status_info['status'],
                    "donation_min": settings.DONATION_MIN,
                    "donation_target": settings.DONATION_TARGET,
                    "donation_currency": settings.DONATION_CURRENCY,
                    "donation_links": {
                        "github_sponsors": settings.SUPPORT_DETAILS['github_sponsors'],
                        "buymeacoffee": settings.SUPPORT_DETAILS['buymeacoffee'],
                    },
                    "message": settings.SUPPORT_STATUS_MESSAGES[status_key],
                },
                "available_services": [
                    "mlbb_api",
                    "mlbb_academy",
                    "mpl_id",
                    "other_mlbb_api",
                ]
            },
            "services": {
                "mlbb_api": {
                    "status": status_info['status'],
                    "message": "MLBB API is currently under maintenance." if not settings.IS_AVAILABLE else "MLBB API is online.",
                    "base_path": "/api/",
                    "endpoints": _get_mlbb_stats_endpoints(request)
                },
                "mlbb_academy": {
                    "status": status_info['status'],
                    "message": "MLBB Academy API is currently under maintenance." if not settings.IS_AVAILABLE else "MLBB Academy API is online.",
                    "base_path": "/api/academy/",
                    "endpoints": _get_mlbb_academy_endpoints(request)
                },
                "mpl_id": {
                    "status": status_info['status'],
                    "message": "MPL ID API is currently under maintenance." if not settings.IS_AVAILABLE else "MPL ID API is online.",
                    "base_path": "/api/mplid/",
                    "endpoints": _get_new_mpl_id_endpoints(request)
                },
                "other_mlbb_api": {
                    "status": status_info['status'],
                    "message": "Other MLBB API is currently under maintenance." if not settings.IS_AVAILABLE else "Other MLBB API is online.",
                    "base_path": "/api/",
                    "endpoints": _get_other_mlbb_api_endpoints(request)
                },
            },
            "links": {
                "api_url": base_api_url if settings.IS_AVAILABLE else settings.MAINTENANCE_INFO_URL,
                "web_url": f"{base_web_url}hero-rank/" if settings.IS_AVAILABLE else settings.MAINTENANCE_INFO_URL,
                "docs": base_docs_url if settings.IS_AVAILABLE else settings.MAINTENANCE_INFO_URL,
            }
        }, status=status.HTTP_200_OK)

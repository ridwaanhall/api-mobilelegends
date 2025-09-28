from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests
from typing import Any, Dict
from apps.mlbb_api.utils import BasePathProvider


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
                    "donation_link": settings.SUPPORT_DETAILS['donation_link']
                },
                "available_endpoints": status_info['available_endpoints']
            },
            "services": {
                "mlbb_api": {
                    "status": status_info['status'],
                    "message": "MLBB API is currently under maintenance." if not settings.IS_AVAILABLE else "MLBB API is online.",
                    "endpoints": _get_available_endpoints(request)
                },
                "mpl_id": {
                    "status": status_info['status'],
                    "message": "MPL ID API is currently under maintenance." if not settings.IS_AVAILABLE else "MPL ID API is online.",
                    "endpoints": _get_new_mpl_id_endpoints(request)
                },
                "mlbb_new_api": {
                    "status": status_info['status'],
                    "message": "MLBB new API is currently under maintenance." if not settings.IS_AVAILABLE else "MLBB API is online.",
                    "endpoints": _get_new_mlbb_api_endpoints(request)
                },
                
            },
            "links": {
                "api_url": "https://mlbb-stats.ridwaanhall.com/api/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
                "web_url": "https://mlbb-stats.ridwaanhall.com/hero-rank/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
                "docs": "https://mlbb-stats-docs.ridwaanhall.com/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            }
        }, status=status.HTTP_200_OK)

def _get_new_mlbb_api_endpoints(request) -> Dict[str, str]:
    """Return new MLBB API endpoints based on API availability."""
    base_url = request.build_absolute_uri('/api/')
    if settings.IS_AVAILABLE:
        return {
            'win_rate': f'{base_url}win-rate/?match-now=100&wr-now=50&wr-future=75',
            'hero_list_new': f'{base_url}hero-list-new/',
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

def _get_available_endpoints(request) -> Dict[str, str]:
    """Return available endpoints based on API availability."""
    base_url = request.build_absolute_uri('/api/')
    if settings.IS_AVAILABLE:
        return {
            'documentation': f'{base_url}',
            'hero_list': f'{base_url}hero-list/',
            'hero_list_new': f'{base_url}hero-list-new/',
            'hero_rank': f'{base_url}hero-rank/',
            'hero_position': f'{base_url}hero-position/',
            'hero_detail': f'{base_url}hero-detail/{{hero_id}}/',
            'hero_detail_stats': f'{base_url}hero-detail-stats/{{main_heroid}}/',
            'hero_skill_combo': f'{base_url}hero-skill-combo/{{hero_id}}/',
            'hero_rate': f'{base_url}hero-rate/{{main_heroid}}/',
            'hero_relation': f'{base_url}hero-relation/{{hero_id}}/',
            'hero_counter': f'{base_url}hero-counter/{{main_heroid}}/',
            'hero_compatibility': f'{base_url}hero-compatibility/{{main_heroid}}/'
        }
    return {'documentation': f'{base_url}'}

HEROES_EN = {
    129: "Zetian", 128: "Kalea", 127: "Lukas", 126: "Suyou", 125: "Zhuxin", 124: "Chip", 123: "Cici", 122: "Nolan", 121: "Ixia", 120: "Arlott", 119: "Novaria",
    118: "Joy", 117: "Fredrinn", 116: "Julian", 115: "Xavier", 114: "Melissa", 113: "Yin", 112: "Floryn",
    111: "Edith", 110: "Valentina", 109: "Aamon", 108: "Aulus", 107: "Natan", 106: "Phoveus", 105: "Beatrix",
    104: "Gloo", 103: "Paquito", 102: "Mathilda", 101: "Yve", 100: "Brody", 99: "Barats", 98: "Khaleed",
    97: "Benedetta", 96: "Luo Yi", 95: "Yu Zhong", 94: "Popol and Kupa", 93: "Atlas", 92: "Carmilla",
    91: "Cecilion", 90: "Silvanna", 89: "Wanwan", 88: "Masha", 87: "Baxia", 86: "Lylia", 85: "Dyrroth",
    84: "Ling", 83: "X.Borg", 82: "Terizla", 81: "Esmeralda", 80: "Guinevere", 79: "Granger", 78: "Khufra",
    77: "Badang", 76: "Faramis", 75: "Kadita", 74: "Minsitthar", 73: "Harith", 72: "Thamuz", 71: "Kimmy",
    70: "Belerick", 69: "Hanzo", 68: "Lunox", 67: "Leomord", 66: "Vale", 65: "Claude", 64: "Aldous",
    63: "Selena", 62: "Kaja", 61: "Chang'e", 60: "Hanabi", 59: "Uranus", 58: "Martis", 57: "Valir",
    56: "Gusion", 55: "Angela", 54: "Jawhead", 53: "Lesley", 52: "Pharsa", 51: "Helcurt", 50: "Zhask",
    49: "Hylos", 48: "Diggie", 47: "Lancelot", 46: "Odette", 45: "Argus", 44: "Grock", 43: "Irithel",
    42: "Harley", 41: "Gatotkaca", 40: "Karrie", 39: "Roger", 38: "Vexana", 37: "Lapu-Lapu", 36: "Aurora",
    35: "Hilda", 34: "Estes", 33: "Cyclops", 32: "Johnson", 31: "Moskov", 30: "Yi Sun-shin", 29: "Ruby",
    28: "Alpha", 27: "Sun", 26: "Chou", 25: "Kagura", 24: "Natalia", 23: "Gord", 22: "Freya", 21: "Hayabusa",
    20: "Lolita", 19: "Minotaur", 18: "Layla", 17: "Fanny", 16: "Zilong", 15: "Eudora", 14: "Rafaela",
    13: "Clint", 12: "Bruno", 11: "Bane", 10: "Franco", 9: "Akai", 8: "Karina", 7: "Alucard", 6: "Tigreal",
    5: "Nana", 4: "Alice", 3: "Saber", 2: "Balmond", 1: "Miya"
}
HEROES_RU = {
    129: "Зетянь", 128: "Калея", 127: "Лукас", 126: "Су Ё", 125: "Чжусинь", 124: "Чип", 123: "Чичи", 122: "Нолан", 121: "Иксия", 120: "Арлотт", 119: "Новария",
    118: "Джой", 117: "Фредринн", 116: "Джулиан", 115: "Ксавьер", 114: "Мелисса", 113: "Инь", 112: "Флорин",
    111: "Эдит", 110: "Валентина", 109: "Эймон", 108: "Аулус", 107: "Натан", 106: "Фовиус", 105: "Беатрис",
    104: "Глу", 103: "Пакито", 102: "Матильда", 101: "Ив", 100: "Броуди", 99: "Бартс", 98: "Халид",
    97: "Бенедетта", 96: "Ло-Йи", 95: "Чонг", 94: "Пополь и Купа", 93: "Атлас", 92: "Кармилла",
    91: "Сесилион", 90: "Сильванна", 89: "Ванван", 88: "Маша", 87: "Баксия", 86: "Лилия", 85: "Дариус",
    84: "Линг", 83: "Икс.Борг", 82: "Теризла", 81: "Эсмеральда", 80: "Гвиневра", 79: "Грейнджер", 78: "Хуфра",
    77: "Баданг", 76: "Фарамис", 75: "Кадита", 74: "Минситтар", 73: "Харит", 72: "Тамуз", 71: "Кимми",
    70: "Белерик", 69: "Ханзо", 68: "Люнокс", 67: "Леоморд", 66: "Вэйл", 65: "Клауд", 64: "Алдос",
    63: "Селена", 62: "Кайя", 61: "Чан'Э", 60: "Ханаби", 59: "Уранус", 58: "Мартис", 57: "Валир",
    56: "Госсен", 55: "Ангела", 54: "Кусака", 53: "Лесли", 52: "Фаша", 51: "Хелкарт", 50: "Заск",
    49: "Хилос", 48: "Дигги", 47: "Ланселот", 46: "Одетта", 45: "Аргус", 44: "Грок", 43: "Иритель",
    42: "Харли", 41: "Гатоткача", 40: "Кэрри", 39: "Роджер", 38: "Вексана", 37: "Лапу-Лапу", 36: "Аврора",
    35: "Хильда", 34: "Эстес", 33: "Циклоп", 32: "Джонсон", 31: "Москов", 30: "Ли Сун Син", 29: "Руби",
    28: "Альфа", 27: "Сан", 26: "Чу", 25: "Кагура", 24: "Наталья", 23: "Горд", 22: "Фрейя", 21: "Хаябуса",
    20: "Лолита", 19: "Минотавр", 18: "Лейла", 17: "Фанни", 16: "Зилонг", 15: "Эйдора", 14: "Рафаэль",
    13: "Клинт", 12: "Бруно", 11: "Бэйн", 10: "Франко", 9: "Акай", 8: "Карина", 7: "Алукард", 6: "Тигрил",
    5: "Нана", 4: "Алиса", 3: "Сабер", 2: "Бальмонд", 1: "Мия"
}

class HeroListView(APIAvailabilityMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lang = request.GET.get('lang', 'en')
        if lang == 'ru':
            return Response(HEROES_RU)
        return Response(HEROES_EN)

class HeroListNewView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path()
        url_hero_list_new = f"{MLBB_URL}{base_path}/2756564"

        lang = request.GET.get('lang', 'en')

        payload = {
            "pageSize": 10000,
            "sorts": [
                {
                    "data": {
                        "field": "hero_id",
                        "order": "desc"
                    },
                    "type": "sequence"
                }
            ],
            "pageIndex": 1,
            "fields": [
                "hero_id",
                "hero.data.head",
                "hero.data.name",
                "hero.data.smallmap",
            ]
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_hero_list_new, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroRankView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path()
        url_1_day = f"{MLBB_URL}{base_path}/2756567"
        url_3_days = f"{MLBB_URL}{base_path}/2756568"
        url_7_days = f"{MLBB_URL}{base_path}/2756569"
        url_15_days = f"{MLBB_URL}{base_path}/2756565"
        url_30_days = f"{MLBB_URL}{base_path}/2756570"

        def create_rank_payload(rank_value):
            return {
                "pageSize": 20,
                "filters": [
                    {"field": "bigrank", "operator": "eq", "value": rank_value},
                    {"field": "match_type", "operator": "eq", "value": "0"}
                ],
                "sorts": [],
                "pageIndex": 1,
                "fields": [
                    "main_hero",
                    "main_hero_appearance_rate",
                    "main_hero_ban_rate",
                    "main_hero_channel",
                    "main_hero_win_rate",
                    "main_heroid",
                    "data.sub_hero.hero",
                    "data.sub_hero.hero_channel",
                    "data.sub_hero.increase_win_rate",
                    "data.sub_hero.heroid"
                ]
            }

        all_rank = create_rank_payload("101")
        epic_rank = create_rank_payload("5")
        legend_rank = create_rank_payload("6")
        mythic_rank = create_rank_payload("7")
        honor_rank = create_rank_payload("8")
        glory_rank = create_rank_payload("9")

        days = request.GET.get('days', '1')
        rank = request.GET.get('rank', 'all')
        page_size = request.GET.get('size', '20')
        page_index = request.GET.get('index', '1')
        sort_field = request.GET.get('sort_field', 'win_rate')
        sort_order = request.GET.get('sort_order', 'desc')
        lang = request.GET.get('lang', 'en')

        sort_field_map = {
            'pick_rate': 'main_hero_appearance_rate',
            'ban_rate': 'main_hero_ban_rate',
            'win_rate': 'main_hero_win_rate'
        }

        url_map = {
            '1': url_1_day,
            '3': url_3_days,
            '7': url_7_days,
            '15': url_15_days,
            '30': url_30_days
        }

        rank_map = {
            'all': all_rank,
            'epic': epic_rank,
            'legend': legend_rank,
            'mythic': mythic_rank,
            'honor': honor_rank,
            'glory': glory_rank
        }

        sort_field = sort_field_map.get(sort_field, 'main_hero_win_rate')
        url = url_map.get(days, url_1_day)
        payload = rank_map.get(rank, all_rank)

        payload['pageSize'] = int(page_size)
        payload['pageIndex'] = int(page_index)
        payload['sorts'] = [
            {"data": {"field": sort_field, "order": sort_order}, "type": "sequence"}
        ]

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroPositionView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        base_path = BasePathProvider.get_base_path()
        url_role_lane = f"{MLBB_URL}{base_path}/2756564"

        role_map = {
            'all': [1, 2, 3, 4, 5, 6],
            'tank': [1],
            'fighter': [2],
            'ass': [3],
            'mage': [4],
            'mm': [5],
            'supp': [6]
        }
        lane_map = {
            'all': [1, 2, 3, 4, 5],
            'exp': [1],
            'mid': [2],
            'roam': [3],
            'jungle': [4],
            'gold': [5]
        }

        role = request.GET.get('role', 'all')
        lane = request.GET.get('lane', 'all')
        page_size = request.GET.get('size', '21')
        page_index = request.GET.get('index', '1')
        lang = request.GET.get('lang', 'en')

        payload = {
            "pageSize": int(page_size),
            "filters": [
                {"field": "<hero.data.sortid>", "operator": "hasAnyOf", "value": role_map.get(role, [1, 2, 3, 4, 5, 6])},
                {"field": "<hero.data.roadsort>", "operator": "hasAnyOf", "value": lane_map.get(lane, [1, 2, 3, 4, 5])}
            ],
            "sorts": [
                {"data": {"field": "hero_id", "order": "desc"}, "type": "sequence"}
            ],
            "pageIndex": int(page_index),
            "fields": ["id", "hero_id", "hero.data.name", "hero.data.smallmap", "hero.data.sortid", "hero.data.roadsort"],
            "object": []
        }

        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url_role_lane, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroDetailView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, hero_id):
        base_path = BasePathProvider.get_base_path()
        url = f"{MLBB_URL}{base_path}/2756564"
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "hero_id", "operator": "eq", "value": hero_id}
            ],
            "sorts": [],
            "pageIndex": 1,
            "object": []
        }
        lang = request.GET.get('lang', 'en')
        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroDetailStatsView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, main_heroid):
        base_path = BasePathProvider.get_base_path()
        url = f"{MLBB_URL}{base_path}/2756567"
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "101"},
                {"field": "match_type", "operator": "eq", "value": "1"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        lang = request.GET.get('lang', 'en')
        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroSkillComboView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, hero_id):
        base_path = BasePathProvider.get_base_path()
        url = f"{MLBB_URL}{base_path}/2674711"
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "hero_id", "operator": "eq", "value": hero_id}
            ],
            "sorts": [],
            "pageIndex": 1,
            "object": [2684183]
        }
        lang = request.GET.get('lang', 'en')
        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroRateView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, main_heroid):
        base_path = BasePathProvider.get_base_path()
        url_past_7_days  = f"{MLBB_URL}{base_path}/2674709"
        url_past_15_days = f"{MLBB_URL}{base_path}/2687909"
        url_past_30_days = f"{MLBB_URL}{base_path}/2690860"

        days = request.GET.get('past-days', '7')
        lang = request.GET.get('lang', 'en')

        url_map = {
            '7': url_past_7_days,
            '15': url_past_15_days,
            '30': url_past_30_days
        }
        url = url_map.get(days, url_past_7_days)

        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "8"},
                {"field": "match_type", "operator": "eq", "value": "1"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroRelationView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, hero_id):
        base_path = BasePathProvider.get_base_path()
        url = f"{MLBB_URL}{base_path}/2756564"
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "hero_id", "operator": "eq", "value": hero_id}
            ],
            "sorts": [],
            "pageIndex": 1,
            "fields": ["hero.data.name"],
            "object": []
        }
        lang = request.GET.get('lang', 'en')
        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroCounterView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, main_heroid):
        base_path = BasePathProvider.get_base_path()
        url = f"{MLBB_URL}{base_path}/2756569"
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "match_type", "operator": "eq", "value": "0"},
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "7"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        lang = request.GET.get('lang', 'en')
        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class HeroCompatibilityView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, main_heroid):
        base_path = BasePathProvider.get_base_path()
        url = f"{MLBB_URL}{base_path}/2756569"
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "match_type", "operator": "eq", "value": "1"},
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "7"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        lang = request.GET.get('lang', 'en')
        headers = MLBBHeaderBuilder.get_lang_header(lang)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return Response(response.json())
        return self.error_response('Failed to fetch data', response.text, status_code=response.status_code)

class WinRateView(APIAvailabilityMixin, ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        match_now = request.GET.get("match-now")
        wr_now = request.GET.get("wr-now")
        wr_future = request.GET.get("wr-future")

        # Validate required parameters
        missing_params = [
            param for param, value in [
                ("match-now", match_now),
                ("wr-now", wr_now),
                ("wr-future", wr_future)
            ] if value is None or value == ""
        ]
        if missing_params:
            return Response({
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": (
                    f"Missing required parameter(s): {', '.join(missing_params)}. "
                    "Please provide all required parameters: match-now, wr-now, and wr-future."
                )
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate and convert input types
        try:
            if "." in str(match_now):
                raise ValueError("match-now must be an integer (no decimals allowed).")
            match_now_int = int(match_now)
            wr_now_float = float(wr_now)
            wr_future_float = float(wr_future)
        except ValueError as e:
            import logging
            logging.error(f"Input validation error: {e}")
            return Response({
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": "Invalid input. Ensure match-now is an integer and wr-now, wr-future are numeric values."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Business logic validations
        if match_now_int < 0:
            return Response({
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "match-now must be a non-negative integer."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not (0 <= wr_now_float <= 100) or not (0 < wr_future_float <= 100):
            return Response({
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "Win rates must be between 0 and 100 (wr-future must be greater than 0)."
            }, status=status.HTTP_400_BAD_REQUEST)

        if wr_future_float <= wr_now_float:
            return Response({
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "The target win rate (wr-future) must be greater than the current win rate (wr-now)."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculation
        current_wins = match_now_int * wr_now_float / 100.0
        wr_future_ratio = wr_future_float / 100.0
        denominator = wr_future_ratio - 1.0
        numerator = current_wins - match_now_int * wr_future_ratio

        if denominator == 0:
            return Response({
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": f"It is not possible to reach a {wr_future_float}% win rate with a finite number of matches."
            }, status=status.HTTP_400_BAD_REQUEST)

        required_matches = numerator / denominator
        required_matches_int = int(required_matches) + (1 if required_matches % 1 > 0 else 0)

        if required_matches_int < 0:
            return Response({
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "The target win rate cannot be achieved with only consecutive wins from your current record."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "match_now": match_now_int,
            "wr_now": wr_now_float,
            "wr_future": wr_future_float,
            "required_no_lose_matches": required_matches_int,
            "message": (
                f"To achieve a win rate of {wr_future_float}%, "
                f"you need {required_matches_int} consecutive wins without any losses."
            )
        }, status=status.HTTP_200_OK)

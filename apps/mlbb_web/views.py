import requests
import os
from django.conf import settings as dj_settings
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from functools import wraps
from typing import Dict

PROD_URL = settings.PROD_URL

HERO_NAME_DICT = {
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

class MLBBWebService:
    @staticmethod
    def get_json(url):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()

    @staticmethod
    def multiply_rates(record, fields):
        for field in fields:
            if field in record:
                record[field] *= 100

    @staticmethod
    def round_rates(record, fields):
        for field in fields:
            if field in record:
                record[field] = round(record[field] * 100, 2)

    @staticmethod
    def map_hero_ids(record, relation_types):
        for relation_type in relation_types:
            for i, hero_id in enumerate(record['data']['relation'][relation_type]['target_hero_id']):
                record['data']['relation'][relation_type]['target_hero_id'][i] = (
                    HERO_NAME_DICT.get(hero_id, 'Unknown') if hero_id != 0 else 'Unknown'
                )

    @staticmethod
    def rename_skill_fields(skilllist):
        for skill in skilllist:
            for skill_detail in skill['skilllist']:
                if 'skillcd&cost' in skill_detail:
                    skill_detail['skillcd_cost'] = skill_detail.pop('skillcd&cost')

    @staticmethod
    def rename_recommendmasterplan_fields(planlist):
        for plan in planlist:
            if '__data' in plan['battleskill']:
                plan['battleskill']['data'] = plan['battleskill'].pop('__data')

    @staticmethod
    def process_sub_hero_rates(sub_hero_list):
        for sub_hero in sub_hero_list:
            MLBBWebService.round_rates(sub_hero, ['hero_appearance_rate', 'hero_win_rate', 'increase_win_rate'])

@api_view(['GET'])
def simple_view(request):
    status_info = settings.API_STATUS_MESSAGES['available'] if settings.IS_AVAILABLE else settings.API_STATUS_MESSAGES['limited']
    data = {
        "code": 200,
        "status": "success",
        "message": "Request processed successfully",
        "service_info": {
            "status": status_info['status'],
            "message": status_info['message'],
            "read_more": "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            "support_message": "You can support us by donating from $1 USD (target: $500 USD) to help enhance API performance and handle high request volumes.",
            "version": settings.API_VERSION,
            "author": "ridwaanhall",
            "available_endpoints": status_info['available_endpoints']
        },
        'new_mlbb_api': _get_new_mlbb_api_endpoints(request),
        "new_mpl_id_api": {
            "status": status_info['status'],
            "message": status_info['message'],
            "available_endpoints": status_info['available_endpoints'],
            "mpl_id_endpoints": _get_new_mpl_id_endpoints(request)
        },
        "data": {
            "donate": "https://github.com/sponsors/ridwaanhall",
            "api_docs": "https://mlbb-stats-docs.ridwaanhall.com/",
            "api_url": "https://mlbb-stats.ridwaanhall.com/api/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            "web_url": "https://mlbb-stats.ridwaanhall.com/hero-rank/" if settings.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/"
        }
    }
    return Response(data)

def _get_new_mlbb_api_endpoints(request) -> Dict[str, str]:
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
        }
    return {}

def favicon_view(request):
    favicon_path = os.path.join(dj_settings.BASE_DIR, 'staticfiles', 'favicon.ico')
    if os.path.exists(favicon_path):
        return FileResponse(open(favicon_path, 'rb'), content_type='image/x-icon')
    else:
        raise Http404('Favicon not found')

class MLBBWebViews:
    @staticmethod
    @web_availability_required
    def hero_list_web(request):
        data = MLBBWebService.get_json(f'{PROD_URL}hero-list/')
        return render(request, 'mlbb_web/hero-list.html', {'data': data})

    @staticmethod
    @web_availability_required
    def hero_rank_web(request):
        days = request.GET.get('days', '1')
        rank = request.GET.get('rank', 'all')
        size = request.GET.get('size', '20')
        index = request.GET.get('index', '1')
        sort_field = request.GET.get('sort_field', 'win_rate')
        sort_order = request.GET.get('sort_order', 'desc')

        url = f'{PROD_URL}hero-rank/?days={days}&rank={rank}&size={size}&index={index}&sort_field={sort_field}&sort_order={sort_order}'
        data = MLBBWebService.get_json(url)
        if not data or 'data' not in data or 'records' not in data['data']:
            return JsonResponse({'error': 'Data not found'}, status=404)

        for record in data['data']['records']:
            MLBBWebService.multiply_rates(record['data'], [
                'main_hero_appearance_rate', 'main_hero_ban_rate', 'main_hero_win_rate'
            ])
            for sub_hero in record['data']['sub_hero']:
                sub_hero['increase_win_rate'] *= 100

        return render(request, 'mlbb_web/hero-rank.html', {
            'data': data,
            'days': days,
            'rank': rank,
            'size': size,
            'index': index,
            'sort_field': sort_field,
            'sort_order': sort_order
        })

    @staticmethod
    @web_availability_required
    def hero_position_web(request):
        role = request.GET.get('role', 'all')
        lane = request.GET.get('lane', 'all')
        size = request.GET.get('size', '21')
        index = request.GET.get('index', '1')

        url = f'{PROD_URL}hero-position/?role={role}&lane={lane}&size={size}&index={index}'
        data = MLBBWebService.get_json(url)
        if data and data['data']['records'] is not None:
            for record in data['data']['records']:
                MLBBWebService.map_hero_ids(record, ['assist', 'strong', 'weak'])

        return render(request, 'mlbb_web/hero-position.html', {
            'data': data,
            'role': role,
            'lane': lane,
            'size': size,
            'index': index
        })

    @staticmethod
    @web_availability_required
    def hero_detail_web(request, hero_id):
        # Hero detail
        data_hero_detail = MLBBWebService.get_json(f'{PROD_URL}hero-detail/{hero_id}/')
        if not data_hero_detail or 'data' not in data_hero_detail or 'records' not in data_hero_detail['data']:
            return JsonResponse({'error': 'Data not found'}, status=404)
        records_data_hero_detail = data_hero_detail['data']['records'][0]['data']

        MLBBWebService.rename_skill_fields(records_data_hero_detail['hero']['data']['heroskilllist'])
        MLBBWebService.rename_recommendmasterplan_fields(records_data_hero_detail['hero']['data']['recommendmasterplan'])

        # Hero stats
        data_hero_detail_stats = MLBBWebService.get_json(f'{PROD_URL}hero-detail-stats/{hero_id}/')
        if not data_hero_detail_stats or 'data' not in data_hero_detail_stats or 'records' not in data_hero_detail_stats['data']:
            return JsonResponse({'error': 'Data not found'}, status=404)
        for record_stats in data_hero_detail_stats['data']['records']:
            MLBBWebService.multiply_rates(record_stats['data'], [
                'main_hero_appearance_rate', 'main_hero_ban_rate', 'main_hero_win_rate'
            ])

        # Hero counter
        data_hero_counter = MLBBWebService.get_json(f'{PROD_URL}hero-counter/{hero_id}/')
        if not data_hero_counter or 'data' not in data_hero_counter or 'records' not in data_hero_counter['data']:
            return JsonResponse({'error': 'Data not found'}, status=404)
        for record in data_hero_counter['data']['records']:
            MLBBWebService.process_sub_hero_rates(record['data']['sub_hero'])
            MLBBWebService.process_sub_hero_rates(record['data']['sub_hero_last'])

        # Hero compatibility
        data_hero_compatibility = MLBBWebService.get_json(f'{PROD_URL}hero-compatibility/{hero_id}/')
        if not data_hero_compatibility or 'data' not in data_hero_compatibility or 'records' not in data_hero_compatibility['data']:
            return JsonResponse({'error': 'Data not found'}, status=404)
        for record in data_hero_compatibility['data']['records']:
            MLBBWebService.process_sub_hero_rates(record['data']['sub_hero'])
            MLBBWebService.process_sub_hero_rates(record['data']['sub_hero_last'])

        return render(request, 'mlbb_web/hero-detail.html', {
            'data': records_data_hero_detail,
            'stats': data_hero_detail_stats,
            'counter': data_hero_counter,
            'compatibility': data_hero_compatibility
        })

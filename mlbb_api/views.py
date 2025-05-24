from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

MLBB_URL = settings.MLBB_URL

# Create your views here.
@api_view(['GET'])
def DocsByRidwaanhall(request):
    return Response(
        {
            "code": 200,
            "status": "success",
            "message": "Request processed successfully",
            "data": {
                "api_docs": "https://mlbb-stats-docs.ridwaanhall.com/",
                "message": "Please visit api_docs for how can you set the API"
            }
        }
    )

# hero list
@api_view(['GET'])
def hero_list(request):
    return Response({

    128: "Kalea", 127: "Lukas", 126: "Suyou", 125: "Zhuxin", 124: "Chip", 123: "Cici", 122: "Nolan", 121: "Ixia", 120: "Arlott", 119: "Novaria",
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
})

@api_view(['GET'])
def hero_rank(request):
    url_1_day = f"{MLBB_URL}gms/source/2669606/2756567"
    url_3_days = f"{MLBB_URL}gms/source/2669606/2756568"
    url_7_days = f"{MLBB_URL}gms/source/2669606/2756569"
    url_15_days = f"{MLBB_URL}gms/source/2669606/2756565"
    url_30_days = f"{MLBB_URL}gms/source/2669606/2756570"
    
    def create_rank_payload(rank_value):
        return {
            "pageSize": 20,
            "filters": [
                {
                    "field": "bigrank",
                    "operator": "eq",
                    "value": rank_value
                },
                {
                    "field": "match_type",
                    "operator":"eq",
                    "value": "0"
                }
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
    
    days = request.query_params.get('days', '1')
    rank = request.query_params.get('rank', 'all')
    page_size = request.query_params.get('size', '20')
    page_index = request.query_params.get('index', '1')
    sort_field = request.query_params.get('sort_field', 'win_rate')
    sort_order = request.query_params.get('sort_order', 'desc')
    lang = request.query_params.get('lang', 'en')

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
        {"data":
            {
                "field": sort_field,
                "order": sort_order
            },
            "type": "sequence"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)
    
@api_view(['GET'])
def hero_position(request):
    url_role_lane = f"{MLBB_URL}gms/source/2669606/2756564"
    
    role_map = {
        'all': [
            1, 
            2, 
            3, 
            4, 
            5, 
            6
        ],
        'tank': [1],
        'fighter': [2],
        'ass': [3],
        'mage': [4],
        'mm': [5],
        'supp': [6]
    }
    
    lane_map = {
        'all': [
            1, 
            2, 
            3, 
            4, 
            5
        ],
        'exp': [1],
        'mid': [2],
        'roam': [3],
        'jungle': [4],
        'gold': [5]
    }
    
    role = request.query_params.get('role', 'all')
    lane = request.query_params.get('lane', 'all')
    page_size = request.query_params.get('size', '21')
    page_index = request.query_params.get('index', '1')
    lang = request.query_params.get('lang', 'en')
    
    payload = {
        "pageSize": int(page_size),
        "filters": [
            {
                "field": "<hero.data.sortid>", 
                "operator": "hasAnyOf", 
                "value": role_map.get(role, [1, 2, 3, 4, 5, 6])
            },
            {
                "field": "<hero.data.roadsort>", 
                "operator": "hasAnyOf", 
                "value": lane_map.get(lane, [1, 2, 3, 4, 5])
            }
        ],
        "sorts": [
            {
                "data": 
                    {
                        "field": "hero_id", 
                        "order": "desc"
                    }, 
                "type": "sequence"
            }
        ],
        "pageIndex": int(page_index),
        "fields": [
            "id", "hero_id", 
            "hero.data.name", 
            "hero.data.smallmap", 
            "hero.data.sortid", 
            "hero.data.roadsort"
        ],
        "object": []
    }
    
    headers = {'Content-Type': 'application/json'}
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url_role_lane, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response(
            {'error': 'Failed to fetch data', 
             'details': response.text
        }, status=response.status_code)

@api_view(['GET'])
def hero_detail(request, hero_id):
    url = f"{MLBB_URL}gms/source/2669606/2756564"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {
                "field": "hero_id", 
                "operator": "eq", 
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": 1,
        "object": []
    }
    
    headers = {'Content-Type': 'application/json'}
    lang = request.query_params.get('lang', 'en')
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)

@api_view(['GET'])
def hero_detail_stats(request, main_heroid):
    url = f"{MLBB_URL}gms/source/2669606/2756567"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {
                "field": "main_heroid", 
                "operator": "eq", 
                "value": main_heroid
            },
            {
                "field": "bigrank", 
                "operator": "eq", 
                "value": "101"
            },
            {
                "field": "match_type",
                "operator": "eq", 
                "value": "1"
            }
        ],
        "sorts": [],
        "pageIndex": 1
    }
    
    headers = {'Content-Type': 'application/json'}
    lang = request.query_params.get('lang', 'en')
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)

@api_view(['GET'])
def hero_skill_combo(request, hero_id):
    url = f"{MLBB_URL}gms/source/2669606/2674711"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {
                "field": "hero_id", 
                "operator": "eq", 
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": 1,
        "object": [2684183]
    }
    
    headers = {'Content-Type': 'application/json'}
    lang = request.query_params.get('lang', 'en')
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)
    
@api_view(['GET'])
def hero_rate(request, main_heroid):
    url_past_7_days  = f"{MLBB_URL}gms/source/2669606/2674709"
    url_past_15_days = f"{MLBB_URL}gms/source/2669606/2687909"
    url_past_30_days = f"{MLBB_URL}gms/source/2669606/2690860"
    
    days = request.query_params.get('past-days', '7')
    lang = request.query_params.get('lang', 'en')
    
    url_map = {
        '7': url_past_7_days,
        '15': url_past_15_days,
        '30': url_past_30_days
    }
    
    url = url_map.get(days, url_past_7_days)
    
    payload = {
        "pageSize": 20,
        "filters": [
            {
                "field": "main_heroid", 
                "operator": "eq", 
                "value": main_heroid
            },
            {
                "field": "bigrank", 
                "operator": "eq", 
                "value": "8"
            },
            {
                "field": "match_type",
                "operator": "eq",
                "value": "1"
            }
        ],
        "sorts": [],
        "pageIndex": 1
    }
    
    headers = {'Content-Type': 'application/json'}
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)

@api_view(['GET'])
def hero_relation(request, hero_id):
    url = f"{MLBB_URL}gms/source/2669606/2756564"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {
                "field": "hero_id", 
                "operator": "eq", 
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": 1,
        "fields": ["hero.data.name"],
        "object": []
    }
    
    headers = {'Content-Type': 'application/json'}
    lang = request.query_params.get('lang', 'en')
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)
    
@api_view(['GET'])
def hero_counter(request, main_heroid):
    url = f"{MLBB_URL}gms/source/2669606/2756569"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {
                "field": "match_type",
                "operator": "eq", 
                 "value": "0"
            },
            {
                "field": "main_heroid", 
                "operator": "eq", 
                "value": main_heroid
            },
            {
                "field": "bigrank", 
                "operator": "eq", 
                "value": "7"
            }
        ],
        "sorts": [],
        "pageIndex": 1
    }
    
    headers = {'Content-Type': 'application/json'}
    lang = request.query_params.get('lang', 'en')
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)
    
@api_view(['GET'])
def hero_compatibility(request, main_heroid):
    url = f"{MLBB_URL}gms/source/2669606/2756569"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {
                "field": "match_type", 
                "operator": "eq", 
                "value": "1"
            },
            {
                "field": "main_heroid", 
                "operator": "eq", 
                "value": main_heroid
            },
            {
                "field": "bigrank", 
                "operator": "eq", 
                "value": "7"
            }
        ],
        "sorts": [],
        "pageIndex": 1
    }
    
    headers = {'Content-Type': 'application/json'}
    lang = request.query_params.get('lang', 'en')
    if lang != 'en':
        headers['x-lang'] = lang
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)

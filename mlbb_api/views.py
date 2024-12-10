from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

MLBB_URL = settings.MLBB_URL

# Create your views here.
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
                {"field": "bigrank", "operator": "eq", "value": rank_value},
                {"field": "match_type", "operator": "eq", "value": "0"}
            ],
            "sorts": [],
            "pageIndex": 1,
            "fields": [
                "main_hero", "main_hero_appearance_rate", "main_hero_ban_rate", "main_hero_channel",
                "main_hero_win_rate", "main_heroid", "data.sub_hero.hero", "data.sub_hero.hero_channel",
                "data.sub_hero.increase_win_rate", "data.sub_hero.heroid"
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

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'error': 'Failed to fetch data', 'details': response.text}, status=response.status_code)
    
@api_view(['GET'])
def hero_position(request):
    url_role_lane = f"{MLBB_URL}gms/source/2669606/2756564"
    
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
    
    role = request.query_params.get('role', 'all')
    lane = request.query_params.get('lane', 'all')
    page_size = request.query_params.get('size', '21')
    page_index = request.query_params.get('index', '1')
    
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
        "fields": [
            "id", "hero_id", "hero.data.name", "hero.data.smallmap", "hero.data.sortid", "hero.data.roadsort"
        ],
        "object": []
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url_role_lane, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'error': 'Failed to fetch data', 'details': response.text}, status=response.status_code)

@api_view(['GET'])
def hero_detail(request, hero_id):
    url = f"{MLBB_URL}gms/source/2669606/2756564"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {"field": "hero_id", "operator": "eq", "value": hero_id}
        ],
        "sorts": [],
        "pageIndex": 1,
        "object": []
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'error': 'Failed to fetch data', 'details': response.text}, status=response.status_code)

@api_view(['GET'])
def hero_detail_stats(request, main_hero_id):
    url = f"{MLBB_URL}gms/source/2669606/2756567"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {"field": "main_heroid", "operator": "eq", "value": main_hero_id},
            {"field": "bigrank", "operator": "eq", "value": "101"},
            {"field": "match_type", "operator": "eq", "value": "1"}
        ],
        "sorts": [],
        "pageIndex": 1
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'error': 'Failed to fetch data', 'details': response.text}, status=response.status_code)

@api_view(['GET'])
def hero_detail_combos(request, hero_id):
    url = f"{MLBB_URL}gms/source/2669606/2674711"
    
    payload = {
        "pageSize": 20,
        "filters": [
            {"field": "hero_id", "operator": "eq", "value": hero_id}
        ],
        "sorts": [],
        "pageIndex": 1,
        "object": [2684183]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'error': 'Failed to fetch data', 'details': response.text}, status=response.status_code)
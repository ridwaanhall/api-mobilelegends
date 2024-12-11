from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

MLBB_URL = settings.MLBB_URL

# Create your views here.
@api_view(['GET'])
def DocsByRidwaanhall(request):
    return Response([
        {
            "endpoint": "GET /api/hero-rank/",
            "description": "This endpoint is used to fetch hero rankings based on various parameters such as days, rank, page size, page index, and sorting options.",
            "query_parameters": {
                "days": {
                    "description": "Number of days for which the data is to be fetched.",
                    "possible_values": [
                        "1",
                        "3",
                        "7",
                        "15",
                        "30"
                    ],
                    "default": "1"
                },
                "rank": {
                    "description": "Rank category for filtering the data.",
                    "possible_values": [
                        "all",
                        "epic",
                        "legend",
                        "mythic",
                        "honor",
                        "glory"
                    ],
                    "default": "all"
                },
                "size": {
                    "description": "Number of records per page.",
                    "possible_values": "From 1 to 126",
                    "default": "20"
                },
                "index": {
                    "description": "Page index for pagination.",
                    "possible_values": "From 1 to 126",
                    "default": "1"
                },
                "sort_field": {
                    "description": "Field by which the data should be sorted.",
                    "possible_values": [
                        "pick_rate",
                        "ban_rate",
                        "win_rate"
                    ],
                    "default": "win_rate"
                },
                "sort_order": {
                    "description": "Order of sorting.",
                    "possible_values": [
                        "asc",
                        "desc"
                    ],
                    "default": "desc"
                }
            },
            "example_request": "GET /api/hero-rank/?days=7&rank=mythic&size=10&index=2&sort_field=pick_rate&sort_order=asc"
        },
        {
            "endpoint": "GET /api/hero-position/",
            "description": "This endpoint is used to fetch hero positions based on various parameters such as role, lane, page size, and page index.",
            "query_parameters": {
                "role": {
                    "description": "Role category for filtering the data.",
                    "possible_values": [
                        "all",
                        "tank",
                        "fighter",
                        "ass",
                        "mage",
                        "mm",
                        "supp"
                    ],
                    "default": "all"
                },
                "lane": {
                    "description": "Lane category for filtering the data.",
                    "possible_values": [
                        "all",
                        "exp",
                        "mid",
                        "roam",
                        "jungle",
                        "gold"
                    ],
                    "default": "all"
                },
                "size": {
                    "description": "Number of records per page.",
                    "possible_values": "From 1 to 126",
                    "default": "21"
                },
                "index": {
                    "description": "Page index for pagination.",
                    "possible_values": "From 1 to 126",
                    "default": "1"
                }
            },
            "example_request": "GET /api/hero-position/?role=tank&lane=mid&size=10&index=2"
        },
        {
            "endpoint": "GET /api/hero-detail/<int:hero_id>/",
            "description": "This endpoint is used to display details of a specific hero identified by `hero_id`.",
            "path_parameters": {
                "hero_id": {
                    "description": "The ID of the hero whose details are to be fetched.",
                    "possible_values": "From 1 to 126",
                    "type": "integer",
                    "required": True
                }
            },
            "example_request": "GET /api/hero-detail/123/"
        },
        {
            "endpoint": "GET /api/hero-detail-stats/<int:main_heroid>/",
            "description": "This endpoint is used to display detailed statistics of a specific hero identified by `main_heroid`.",
            "path_parameters": {
                "main_heroid": {
                    "description": "The ID of the main hero whose detailed statistics are to be fetched.",
                    "possible_values": "From 1 to 126",
                    "type": "integer",
                    "required": True
                }
            },
            "example_request": "GET /api/hero-detail-stats/123/"
        },
        {
            "endpoint": "GET /api/hero-skill-combo/<int:hero_id>/",
            "description": "This endpoint is used to display skill combinations of a specific hero identified by `hero_id`.",
            "path_parameters": {
                "hero_id": {
                    "description": "The ID of the hero whose skill combinations are to be fetched.",
                    "possible_values": "From 1 to 126",
                    "type": "integer",
                    "required": True
                }
            },
            "example_request": "GET /api/hero-skill-combo/123/"
        },
        {
            "endpoint": "GET /api/hero-rate/<int:main_heroid>/",
            "description": "This endpoint is used to rate a specific hero identified by `main_heroid`.",
            "path_parameters": {
                "main_heroid": {
                    "description": "The ID of the main hero whose rating is to be fetched.",
                    "possible_values": "From 1 to 126",
                    "type": "integer",
                    "required": True
                }
            },
            "query_parameters": {
                "past-days": {
                    "description": "Number of past days for which the data is to be fetched.",
                    "possible_values": [
                        "7",
                        "15",
                        "30"
                    ],
                    "default": "7"
                }
            },
            "example_request": "GET /api/hero-rate/123/?past-days=15"
        },
        {
            "endpoint": "GET /api/hero-relation/<int:hero_id>/",
            "description": "This endpoint is used to display relationships of a specific hero identified by `hero_id`.",
            "path_parameters": {
                "hero_id": {
                    "description": "The ID of the hero whose relationships are to be fetched.",
                    "possible_values": "From 1 to 126",
                    "type": "integer",
                    "required": True
                }
            },
            "example_request": "GET /api/hero-relation/123/"
        },
        {
            "endpoint": "GET /api/hero-counter/<int:main_heroid>/",
            "description": "This endpoint is used to display counter information of a specific hero identified by `main_heroid`.",
            "path_parameters": {
                "main_heroid": {
                    "description": "The ID of the main hero whose counter information is to be fetched.",
                    "possible_values": "From 1 to 126",
                    "type": "integer",
                    "required": True
                }
            },
            "example_request": "GET /api/hero-counter/123/"
        },
        {
            "endpoint": "GET /api/hero-compatibility/<int:main_heroid>/",
            "description": "This endpoint is used to display compatibility information of a specific hero identified by `main_heroid`.",
            "path_parameters": {
                "main_heroid": {
                    "description": "The ID of the main hero whose compatibility information is to be fetched.",
                    "possible_values": "From 1 to 126",
                    "type": "integer",
                    "required": True
                }
            },
            "example_request": "GET /api/hero-compatibility/123/"
        }
    ])


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
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({
            'error': 'Failed to fetch data', 
            'details': response.text
        }, status=response.status_code)
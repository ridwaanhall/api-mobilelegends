"""MLBB API Router for FastAPI"""
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import requests
import config
from utils import BasePathProvider, MLBBHeaderBuilder

router = APIRouter()

MLBB_URL = config.MLBB_URL


def check_availability():
    """Check if API is available"""
    if not config.IS_AVAILABLE:
        status_info = config.API_STATUS_MESSAGES['limited']
        raise HTTPException(
            status_code=503,
            detail={
                'error': 'Service Unavailable',
                'status': status_info['status'],
                'message': status_info['message'],
                'available_endpoints': status_info['available_endpoints']
            }
        )


def _get_available_endpoints(request: Request) -> Dict[str, str]:
    """Return available endpoints based on API availability."""
    base_url = str(request.base_url) + 'api/'
    if config.IS_AVAILABLE:
        return {
            'documentation': f'{base_url}',
            'hero_list': f'{base_url}hero-list/',
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


def _get_new_mlbb_api_endpoints(request: Request) -> Dict[str, str]:
    """Return new MLBB API endpoints based on API availability."""
    base_url = str(request.base_url) + 'api/'
    if config.IS_AVAILABLE:
        return {
            'win_rate': f'{base_url}win-rate/?match-now=100&wr-now=50&wr-future=75',
        }
    return {}


@router.get("/")
async def api_endpoints(request: Request):
    """Root endpoint showing API documentation and available endpoints"""
    status_info = config.API_STATUS_MESSAGES['available'] if config.IS_AVAILABLE else config.API_STATUS_MESSAGES['limited']
    return {
        "code": 200,
        "status": "success",
        "message": "Request processed successfully",
        "meta": {
            "version": config.API_VERSION,
            "author": "ridwaanhall",
            "support": {
                "status": status_info['status'],
                "message": status_info['message'],
                "support_message": config.SUPPORT_DETAILS['support_message'],
                "donation_link": config.SUPPORT_DETAILS['donation_link']
            },
            "available_endpoints": status_info['available_endpoints']
        },
        "services": {
            "mlbb_api": {
                "status": status_info['status'],
                "message": "MLBB API is currently under maintenance." if not config.IS_AVAILABLE else "MLBB API is online.",
                "endpoints": _get_available_endpoints(request)
            },
            "mlbb_new_api": {
                "status": status_info['status'],
                "message": "MLBB new API is currently under maintenance." if not config.IS_AVAILABLE else "MLBB API is online.",
                "endpoints": _get_new_mlbb_api_endpoints(request)
            },
        },
        "links": {
            "api_url": "https://mlbb-stats.ridwaanhall.com/api/" if config.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            "web_url": "https://mlbb-stats.ridwaanhall.com/hero-rank/" if config.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            "docs": "https://mlbb-stats-docs.ridwaanhall.com/" if config.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            "FastAPI Docs": "https://mlbb-stats.ridwaanhall.com/docs" if config.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            "ReDoc": "https://mlbb-stats.ridwaanhall.com/redoc" if config.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
            "github": "https://github.com/ridwaanhall/api-mobilelegends" if config.IS_AVAILABLE else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
        }
    }


@router.get("/docs/")
async def api_docs(request: Request):
    """Docs endpoint (same as root)"""
    return await api_endpoints(request)


@router.get("/hero-list/")
async def hero_list_new(lang: str = Query(default="en")):
    """Get new hero list from MLBB API"""
    check_availability()
    base_path = BasePathProvider.get_base_path()
    url_hero_list_new = f"{MLBB_URL}{base_path}/2756564"

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
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-rank/")
async def hero_rank(
    days: str = Query(default="1"),
    rank: str = Query(default="all"),
    size: str = Query(default="20"),
    index: str = Query(default="1"),
    sort_field: str = Query(default="win_rate"),
    sort_order: str = Query(default="desc"),
    lang: str = Query(default="en")
):
    """Get hero rank data"""
    check_availability()
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

    payload['pageSize'] = int(size)
    payload['pageIndex'] = int(index)
    payload['sorts'] = [
        {"data": {"field": sort_field, "order": sort_order}, "type": "sequence"}
    ]

    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-position/")
async def hero_position(
    role: str = Query(default="all"),
    lane: str = Query(default="all"),
    size: str = Query(default="21"),
    index: str = Query(default="1"),
    lang: str = Query(default="en")
):
    """Get heroes by role and lane position"""
    check_availability()
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

    payload = {
        "pageSize": int(size),
        "filters": [
            {"field": "<hero.data.sortid>", "operator": "hasAnyOf", "value": role_map.get(role, [1, 2, 3, 4, 5, 6])},
            {"field": "<hero.data.roadsort>", "operator": "hasAnyOf", "value": lane_map.get(lane, [1, 2, 3, 4, 5])}
        ],
        "sorts": [
            {"data": {"field": "hero_id", "order": "desc"}, "type": "sequence"}
        ],
        "pageIndex": int(index),
        "fields": ["id", "hero_id", "hero.data.name", "hero.data.smallmap", "hero.data.sortid", "hero.data.roadsort"],
        "object": []
    }

    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url_role_lane, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-detail/{hero_id}")
async def hero_detail(hero_id: int, lang: str = Query(default="en")):
    """Get detailed hero information"""
    check_availability()
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
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-detail-stats/{main_heroid}")
async def hero_detail_stats(main_heroid: int, lang: str = Query(default="en")):
    """Get hero statistics"""
    check_availability()
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
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-skill-combo/{hero_id}")
async def hero_skill_combo(hero_id: int, lang: str = Query(default="en")):
    """Get hero skill combo information"""
    check_availability()
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
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-rate/{main_heroid}")
async def hero_rate(
    main_heroid: int,
    past_days: str = Query(default="7", alias="past-days"),
    lang: str = Query(default="en")
):
    """Get hero rate over time"""
    check_availability()
    base_path = BasePathProvider.get_base_path()
    url_past_7_days = f"{MLBB_URL}{base_path}/2674709"
    url_past_15_days = f"{MLBB_URL}{base_path}/2687909"
    url_past_30_days = f"{MLBB_URL}{base_path}/2690860"

    url_map = {
        '7': url_past_7_days,
        '15': url_past_15_days,
        '30': url_past_30_days
    }
    url = url_map.get(past_days, url_past_7_days)

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
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-relation/{hero_id}")
async def hero_relation(hero_id: int, lang: str = Query(default="en")):
    """Get hero relation information"""
    check_availability()
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
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-counter/{main_heroid}")
async def hero_counter(main_heroid: int, lang: str = Query(default="en")):
    """Get hero counter information"""
    check_availability()
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
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})


@router.get("/hero-compatibility/{main_heroid}")
async def hero_compatibility(main_heroid: int, lang: str = Query(default="en")):
    """Get hero compatibility information"""
    check_availability()
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
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail={'error': 'Failed to fetch data', 'details': response.text})




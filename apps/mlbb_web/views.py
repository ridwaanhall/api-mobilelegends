"""
MLBB Web Views with Dynamic Hero Names

This module now uses dynamic hero name fetching from the API instead of a static dictionary.
Hero names are automatically cached for 24 hours to improve performance.

Key features:
- Automatic hero name fetching from API
- 24-hour caching to reduce API calls
- Fallback mechanism if API is unavailable
- Manual cache refresh capability
- Management command: python manage.py refresh_heroes
- API endpoint: POST /refresh-heroes/ to refresh cache manually

When new heroes are added to the game, the cache will automatically update
within 24 hours, or can be manually refreshed using the command or endpoint.
"""

import requests
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from django.core.cache import cache
import logging
from apps.core.utils import web_availability_required

logger = logging.getLogger(__name__)

PROD_URL = settings.PROD_URL

# Cache key for hero names
HERO_CACHE_KEY = 'mlbb_hero_names'
HERO_CACHE_TIMEOUT = 86400  # 24 hours in seconds

def get_hero_names_dict():
    """
    Fetch hero names from API and cache them.
    Returns a dictionary mapping hero_id to hero_name.
    """
    # Try to get from cache first
    hero_dict = cache.get(HERO_CACHE_KEY)
    if hero_dict is not None:
        return hero_dict
    
    try:
        # Fetch from API
        response = requests.get(f'{PROD_URL}hero-list/', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and 'data' in data and 'records' in data['data']:
                # Create hero dictionary from API response
                hero_dict = {}
                for record in data['data']['records']:
                    hero_id = record['data']['hero_id']
                    hero_name = record['data']['hero']['data']['name']
                    hero_dict[hero_id] = hero_name
                
                # Cache the result
                cache.set(HERO_CACHE_KEY, hero_dict, HERO_CACHE_TIMEOUT)
                logger.info(f"Successfully fetched and cached {len(hero_dict)} heroes")
                return hero_dict
    except Exception as e:
        logger.error(f"Error fetching hero list from API: {e}")
    
    # Fallback to basic hero dictionary if API fails
    fallback_dict = {
        1: "Miya", 2: "Balmond", 3: "Saber", 4: "Alice", 5: "Nana",
        6: "Tigreal", 7: "Alucard", 8: "Karina", 9: "Akai", 10: "Franco",
        # Add more basic heroes as needed
    }
    logger.warning("Using fallback hero dictionary due to API failure")
    return fallback_dict

def refresh_hero_cache():
    """
    Force refresh of hero names cache.
    Returns True if successful, False otherwise.
    """
    try:
        # Clear existing cache
        cache.delete(HERO_CACHE_KEY)
        
        # Fetch fresh data
        hero_dict = get_hero_names_dict()
        
        if hero_dict and len(hero_dict) > 0:
            logger.info(f"Hero cache refreshed successfully with {len(hero_dict)} heroes")
            return True
    except Exception as e:
        logger.error(f"Error refreshing hero cache: {e}")
    
    return False

def get_hero_cache_info():
    """
    Get information about the current hero cache.
    Returns a dictionary with cache statistics.
    """
    try:
        hero_dict = get_hero_names_dict()
        
        if hero_dict:
            latest_hero_id = max(hero_dict.keys())
            latest_hero_name = hero_dict[latest_hero_id]
            
            return {
                'total_heroes': len(hero_dict),
                'latest_hero_id': latest_hero_id,
                'latest_hero_name': latest_hero_name,
                'cache_active': True,
                'heroes': hero_dict
            }
    except Exception as e:
        logger.error(f"Error getting hero cache info: {e}")
    
    return {
        'total_heroes': 0,
        'latest_hero_id': None,
        'latest_hero_name': None,
        'cache_active': False,
        'heroes': {}
    }

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
        hero_names = get_hero_names_dict()
        for relation_type in relation_types:
            for i, hero_id in enumerate(record['data']['relation'][relation_type]['target_hero_id']):
                if hero_id != 0:
                    # Create an object with both ID and name for template use
                    record['data']['relation'][relation_type]['target_hero_id'][i] = {
                        'id': hero_id,
                        'name': hero_names.get(hero_id, 'Unknown')
                    }
                else:
                    # For unknown heroes (ID = 0)
                    record['data']['relation'][relation_type]['target_hero_id'][i] = {
                        'id': 0,
                        'name': 'Unknown'
                    }

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

def favicon_view(request):
    favicon_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'favicon.ico')
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

    @staticmethod
    def refresh_hero_cache_view(request):
        """
        API endpoint to manually refresh hero cache and get cache information.
        GET: Returns current cache status and information
        POST: Refreshes the cache and returns updated information
        """
        if request.method == 'POST':
            success = refresh_hero_cache()
            cache_info = get_hero_cache_info()
            
            if success and cache_info['cache_active']:
                return JsonResponse({
                    'success': True,
                    'message': f'Hero cache refreshed successfully',
                    'cache_info': {
                        'total_heroes': cache_info['total_heroes'],
                        'latest_hero_id': cache_info['latest_hero_id'],
                        'latest_hero_name': cache_info['latest_hero_name'],
                        'cache_timeout_hours': HERO_CACHE_TIMEOUT / 3600
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Failed to refresh hero cache'
                }, status=500)
        
        # GET request - show current cache status
        cache_info = get_hero_cache_info()
        return JsonResponse({
            'cache_status': 'active' if cache_info['cache_active'] else 'inactive',
            'cache_info': {
                'total_heroes': cache_info['total_heroes'],
                'latest_hero_id': cache_info['latest_hero_id'],
                'latest_hero_name': cache_info['latest_hero_name'],
                'cache_timeout_hours': HERO_CACHE_TIMEOUT / 3600
            },
            'message': 'Use POST request to refresh cache',
            'endpoints': {
                'refresh': 'POST /refresh-heroes/',
                'status': 'GET /refresh-heroes/',
                'management_command': 'python manage.py refresh_heroes'
            }
        })

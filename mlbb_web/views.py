import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings


LOCAL_URL = settings.LOCAL_URL

# Create your views here.
def simple_view(request):
    data = {
        "code": 200,
        "status": "ok",
        "message": "Hello ridwaanhall",
        "data": {
            "api-url": "https://api-pddikti.vercel.app/api/",
            "web-url": "https://api-pddikti.vercel.app/"
        }
    }
    return JsonResponse(data)

HERO_NAME_DICT = {
    126: "Suyou", 125: "Zhuxin", 124: "Chip", 123: "Cici", 122: "Nolan", 121: "Ixia", 120: "Arlott", 119: "Novaria",
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

def hero_rank_web(request):
    days = request.GET.get('days', '1')
    rank = request.GET.get('rank', 'all')
    size = request.GET.get('size', '20')
    index = request.GET.get('index', '1')
    sort_field = request.GET.get('sort_field', 'win_rate')
    sort_order = request.GET.get('sort_order', 'desc')

    response = requests.get(f'{LOCAL_URL}hero-rank/?days={days}&rank={rank}&size={size}&index={index}&sort_field={sort_field}&sort_order={sort_order}')
    if response.status_code != 200:
        return JsonResponse({'error': 'Data not found'}, status=404)
    data = response.json()
    if data is None or 'data' not in data or 'records' not in data['data']:
        return JsonResponse({'error': 'Data not found'}, status=404)

    # Convert rates to percentages
    for record in data['data']['records']:
        record['data']['main_hero_appearance_rate'] *= 100
        record['data']['main_hero_ban_rate'] *= 100
        record['data']['main_hero_win_rate'] *= 100
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

def hero_position_web(request):
    role = request.GET.get('role', 'all')
    lane = request.GET.get('lane', 'all')
    size = request.GET.get('size', '21')
    index = request.GET.get('index', '1')

    response = requests.get(f'{LOCAL_URL}hero-position/?role={role}&lane={lane}&size={size}&index={index}')
    data = response.json()

    # Map hero IDs to names
    if data['data']['records'] is not None:
        for record in data['data']['records']:
            for relation_type in ['assist', 'strong', 'weak']:
                for i, hero_id in enumerate(record['data']['relation'][relation_type]['target_hero_id']):
                    if hero_id != 0:
                        record['data']['relation'][relation_type]['target_hero_id'][i] = HERO_NAME_DICT.get(hero_id, 'Unknown')
                    else:
                        record['data']['relation'][relation_type]['target_hero_id'][i] = 'Unknown'

    return render(request, 'mlbb_web/hero-position.html', {
        'data': data,
        'role': role,
        'lane': lane,
        'size': size,
        'index': index
    })

def hero_detail_web(request, hero_id):
    response = requests.get(f'{LOCAL_URL}hero-detail/{hero_id}/')
    if response.status_code != 200:
        return JsonResponse({'error': 'Data not found'}, status=404)
    data = response.json()
    if data is None or 'data' not in data or 'records' not in data['data']:
        return JsonResponse({'error': 'Data not found'}, status=404)

    # Extract the data inside records
    records_data = data['data']['records'][0]['data']

    # Rename 'skillcd&cost' to 'skillcd_cost' in the skill details
    for skill in records_data['hero']['data']['heroskilllist']:
        for skill_detail in skill['skilllist']:
            skill_detail['skillcd_cost'] = skill_detail.pop('skillcd&cost')

    return render(request, 'mlbb_web/hero-detail.html', {'data': records_data})

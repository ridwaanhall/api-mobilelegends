from decouple import config

# API Availability Control
IS_AVAILABLE = config('IS_AVAILABLE', default=True, cast=bool)
DATE_AVAILABLE = config('DATE_AVAILABLE', default='February 11, 2026')

SUPPORT_DETAILS = {
    'support_message': 'You can support us by donating from $1 USD (target: $500 USD) to help enhance API performance and handle high request volumes.',
    'github_sponsors': 'https://github.com/sponsors/ridwaanhall',
    'buymeacoffee': 'https://www.buymeacoffee.com/ridwaanhall',
    'donation_link': 'https://github.com/sponsors/ridwaanhall',
    'id_zone_ori': 'original server: 688700997 (8742)',
    'id_zone_adv': 'advanced server: 1149309666 (57060)',
}

WEB_BASE_URL = config('WEB_BASE_URL', default='https://mlbb-stats.rone.dev/')
API_BASE_URL = config('API_BASE_URL', default=f'{WEB_BASE_URL}api/')
DOCS_BASE_URL = config('DOCS_BASE_URL', default='https://mlbb-stats-docs.rone.dev/')

MAINTENANCE_INFO_URL = config(
    'MAINTENANCE_INFO_URL',
    default='https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/'
)

DONATION_MIN = config('DONATION_MIN', default=1, cast=int)
DONATION_TARGET = config('DONATION_TARGET', default=500, cast=int)
DONATION_CURRENCY = config('DONATION_CURRENCY', default='USD')

SUPPORT_STATUS_MESSAGES = {
    'limited': config(
        'SUPPORT_MESSAGE_LIMITED',
        default='API is currently in maintenance mode. Donations help cover hosting and performance scaling.'
    ),
    'available': config(
        'SUPPORT_MESSAGE_AVAILABLE',
        default='All API endpoints are fully operational. Donations help cover hosting and performance scaling.'
    ),
}

# API Status Messages
API_STATUS_MESSAGES = {
    'limited': {
        'status': 'limited',
        'message': f'API is currently in maintenance mode. Will available {DATE_AVAILABLE}.',
        'available_endpoints': ['Base API']
    },
    'available': {
        'status': 'available',
        'message': 'All API endpoints are fully operational.',
        'available_endpoints': ['All endpoints']
    }
}

API_VERSION = config('API_VERSION', default='1.6.0')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

MLBB_URL = config('MLBB_URL')
MLBB_URL_V2 = config('MLBB_URL_V2')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Set base URL based on DEBUG mode
if DEBUG:
    PROD_URL = 'http://127.0.0.1:8000/api/'
else:
    PROD_URL = config('PROD_URL', default=API_BASE_URL)

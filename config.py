"""FastAPI Configuration Module"""
from decouple import config
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent

# API Availability Control
IS_AVAILABLE = config('IS_AVAILABLE', default=True, cast=bool)

SUPPORT_DETAILS = {
    'support_message': 'You can support us by donating from $1 USD (target: $500 USD) to help enhance API performance and handle high request volumes.',
    'donation_link': 'https://github.com/sponsors/ridwaanhall'
}

# API Status Messages
API_STATUS_MESSAGES = {
    'limited': {
        'status': 'limited',
        'message': 'API is currently in maintenance mode. Will available August 28, 2025.',
        'available_endpoints': ['Base API']
    },
    'available': {
        'status': 'available',
        'message': 'All API endpoints are fully operational.',
        'available_endpoints': ['All endpoints']
    }
}

API_VERSION = config('API_VERSION', default='1.2.0')

# Security Settings
SECRET_KEY = config('SECRET_KEY')
MLBB_URL = config('MLBB_URL')

# Debug and Production
DEBUG = config('DEBUG', default=False, cast=bool)

# Set base URL based on DEBUG mode
if DEBUG:
    PROD_URL = 'http://127.0.0.1:8000/api/'
else:
    PROD_URL = config('PROD_URL')

# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://mlbb-stats.ridwaanhall.com",
    "https://mlbb-stats-docs.ridwaanhall.com",
    "https://*.vercel.app",
    "https://*.ridwaanhall.com",
]

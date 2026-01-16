from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

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

WEB_BASE_URL = config('WEB_BASE_URL', default='https://mlbb-stats.ridwaanhall.com/')
API_BASE_URL = config('API_BASE_URL', default=f'{WEB_BASE_URL}api/')
DOCS_BASE_URL = config('DOCS_BASE_URL', default='https://mlbb-stats-docs.ridwaanhall.com/')

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

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

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

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = [
        '.vercel.app',
        '.ridwaanhall.com',
        '.rone.dev',
    ]

# Security settings for production
if not DEBUG:
    # HTTPS Security
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie Security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Additional security settings
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Force HTTPS for all requests
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    
    'apps.core',
    'apps.mlbb_api',
    'apps.mlbb_web',
    'apps.mpl_api',
    'apps.academy_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MLBB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "apps.core.context_processors.base_urls",
            ],
        },
    },
]

WSGI_APPLICATION = 'MLBB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/' # for local development

# STATICFILES_DIRS = [
#     BASE_DIR / "static", # for local development
# ]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ],
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',
#     ],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 100,
# }

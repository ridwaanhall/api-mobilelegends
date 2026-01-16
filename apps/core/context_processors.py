from django.conf import settings

def base_urls(request):
    return {
        "WEB_BASE_URL": settings.WEB_BASE_URL,
        "API_BASE_URL": settings.API_BASE_URL,
        "DOCS_BASE_URL": settings.DOCS_BASE_URL,
    }

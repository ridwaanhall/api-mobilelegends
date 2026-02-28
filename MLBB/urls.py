"""
URL configuration for MLBB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.http import HttpResponseRedirect
from apps.core.views import robots_txt, sitemap_xml

def redirect_to_api(request):
    return HttpResponseRedirect('/api/')

urlpatterns = [
    
    path('', redirect_to_api, name='redirect_to_api'),

    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    
    path('api/', include('apps.mlbb_api.urls')),
    path('api/', include('apps.mpl_api.urls')),
    path('api/', include('apps.academy_api.urls')),
    
    path('', include('apps.mlbb_web.urls')),
    
]

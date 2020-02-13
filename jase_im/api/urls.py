"""jase_im URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django_xmlrpc.views import handle_xmlrpc

from api.views import images, auth, parsers, wallpaper, ip

router = DefaultRouter()

# app_name = 'api'
urlpatterns = [
    # url(r'^v1/', include(router.urls)),
    url(r'^(?P<version>(v1))/image/(?P<slug>.+)/', images.ImageView.as_view(), name='image-detail'),
    url(r'^(?P<version>(v1))/image/', images.ImageView.as_view(), name='image'),
    url(r'^(?P<version>(v1))/auth/', auth.Auth.as_view(), name='auth'),
    url(r'^(?P<version>(v1))/parser/', parsers.Parser.as_view(), name='parser'),
    url(r'^(?P<version>(v1))/bing-daily-wallpaper/', wallpaper.Bing_Daily_Wallpaper.as_view(), name='bing_wallpaper'),
    url(r'^metaweblog/', handle_xmlrpc, name='metaweblog'),
    url(r'^(?P<version>(v1))/ip/v4', ip.Request_IPv4.as_view(), name='ipv4'),
]

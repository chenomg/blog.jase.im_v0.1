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

from api import views

router = DefaultRouter()

# app_name = 'api'
urlpatterns = [
    # url(r'^v1/', include(router.urls)),
    url(r'^(?P<version>(v1))/image/(?P<slug>.+)/', views.ImageView.as_view(), name='image-get'),
    url(r'^(?P<version>(v1))/image/', views.ImageView.as_view(), name='image-post'),
    url(r'^(?P<version>(v1))/auth/', views.Auth.as_view(), name='auth'),
    url(r'^(?P<version>(v1))/parser/', views.Parser.as_view(), name='parser'),
    url(r'^(?P<version>(v1))/bing-daily-wallpaper/', views.Bing_Daily_Wallpaper.as_view(), name='bing_wallpaper'),
]

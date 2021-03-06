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
from django.conf.urls import url, include, handler404
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
from blog import views
from django.conf import settings
from django.views.static import serve

handler404 = views.page_not_found
urlpatterns = [
    # url(r'^$', RedirectView.as_view(url='/blog/')),
    url(r'^$', include('homepage.urls'), name='homepage'),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^mdeditor/', include('mdeditor.urls')),
    url(r'^djga/', include('google_analytics.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^.well-known/acme-challenge/', include('ssl_verify.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        # For django versions before 2.0:
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

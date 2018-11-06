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
from django.conf.urls.static import static
from django.conf import settings
from blog import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^tags/', views.tag_list_show, name='tag_list_show'),
    url(r'^tag/(?P<tag_slug>.+)/', views.tag_show, name='tag_show'),
    url(r'^post/(?P<post_title_slug>.+)/$',
        views.post_detail,
        name='post_detail'),
    url(r'^category/', views.category, name='category'),
    url(r'^archive/', views.archive, name='archive'),
    url(
        r'^mdeditor/',
        include('mdeditor.urls'),
    )
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

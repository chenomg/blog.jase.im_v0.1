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
    url(r'^about/$', views.about, name='about'),
    url(r'^tags/$', views.tag_list_show, name='tag_list_show'),
    url(r'^tag/(?P<tag_slug>.+)/$', views.tag_show, name='tag_show'),
    url(r'^post/add/$', views.add_post, name='addpost'),
    url(r'^post/update/(?P<slug>.+)/$', views.update_post, name='update_post'),
    url(r'^post/(?P<slug>.+)/$', views.post_detail, name='post_detail'),
    url(r'^category/$', views.category, name='category'),
    url(r'^register_profile/$', views.register_profile,
        name='register_profile'),
    url(r'^comment_submit/$', views.comment_submit, name='comment_submit'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^user/(?P<username>.+)/$', views.user_show, name='user_show'),
    url(
        r'^mdeditor/',
        include('mdeditor.urls'),
    ),
    # api
    url(r'^api/v1/posts/$', views.post_collection, name='api_posts'),
    url(r'^api/v1/posts/(?P<pk>.+)/$', views.post_element, name='api_post_element'),
]

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
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add-new-post/$', views.add_new_post, name='add_new_post'),
    url(r'^components-blog-posts/$', views.components_blog_posts, name='components_blog_posts'),
]

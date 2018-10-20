from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Category, Tag, Post, Archive


def index(request):
    posts = Post.objects.all()
    context_dic = {'posts': posts}
    context_dic['most_viewed_posts'] = Post.objects.order_by('-views')[:5]
    return render(request, 'blog/index.html', context=context_dic)


def about(request):
    context_dic = {}
    return render(request, 'blog/about.html', context=context_dic)

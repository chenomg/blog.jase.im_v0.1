from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Category, Tag, Post, Archive


def index(request):
    posts = Post.objects.all().order_by('-modified_time')
    posts_per_page = 7
    paginator = Paginator(posts, posts_per_page)
    pages_count = paginator.num_pages
    page_id = request.GET.get('page', '1')
    if int(page_id) > pages_count:
        page_id = pages_count
    selected_page = paginator.page(page_id)
    context_dic = {
        'posts': selected_page,
        'is_detail': False,
        'pages_total': pages_count,
        'page_current': page_id,
    }
    return render(request, 'blog/index.html', context=context_dic)


def about(request):
    context_dic = {}
    return render(request, 'blog/about.html', context=context_dic)


def post_detail(request, post_title_slug):
    try:
        post = Post.objects.get(title_slug=post_title_slug)
    except Exception:
        post = None
    print(post)
    context = {'post': post, 'is_detail': True}
    return render(request, 'blog/post_detail.html', context=context)


def category(request):
    categories = Category.objects.all().order_by('-name')
    posts = Post.objects.all()
    context = {'categories': categories, 'posts': posts, 'is_detail': False}
    return render(request, 'blog/category.html', context=context)

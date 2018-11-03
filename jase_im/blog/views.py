from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from blog.models import Category, Tag, Post, Archive, Comment
from .forms import CommentForm
import datetime


def index(request):
    posts = Post.objects.all().order_by('-modified_time')
    posts_per_page = 3
    paginator = Paginator(posts, posts_per_page)
    pages_count = paginator.num_pages
    page_id = int(request.GET.get('page', '1'))
    page_previous_id = 1
    page_next_id = pages_count
    if page_id == 1:
        page_previous = False
    else:
        page_previous = True
        page_previous_id = page_id - 1
    if page_id == pages_count:
        page_next = False
    else:
        page_next = True
        page_next_id = page_id + 1
    if page_id > pages_count:
        page_id = pages_count
    selected_page = paginator.page(page_id)
    context_dic = {
        'posts': selected_page,
        'pages_total': pages_count,
        'page_current': page_id,
        'page_previous': page_previous,
        'page_previous_id': page_previous_id,
        'page_next': page_next,
        'page_next_id': page_next_id,
    }
    return render(request, 'blog/index.html', context=context_dic)


def about(request):
    context_dic = {}
    return render(request, 'blog/about.html', context=context_dic)


def post_detail(request, post_title_slug):
    post = get_object_or_404(Post, title_slug=post_title_slug)
    comments = Post.objects.get(
        title_slug=post_title_slug).comment_set.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            comment = Comment.objects.create(
                name=name, content=content, email=email, post=post)
        return HttpResponseRedirect(
            reverse('blog:post_detail', args=[post.title_slug]))
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'is_detail': True
    }
    return render(request, 'blog/post_detail.html', context=context)


def category(request):
    categories = Category.objects.all().order_by('-name')
    posts = Post.objects.all()
    context = {'categories': categories, 'posts': posts}
    return render(request, 'blog/category.html', context=context)


def archive(request):
    posts = Post.objects.all().order_by('created_time')
    dates = set([(p.created_time.year, p.created_time.month) for p in posts])
    dates = sorted([datetime.date(dt[0], dt[1], 1) for dt in dates])
    context = {'posts': posts, 'dates': dates}
    return render(request, 'blog/archive.html', context=context)


def tag_list_show(request):
    tags = Tag.objects.all().order_by('slug')
    context = {'tags': tags}
    return render(request, 'blog/tags_list_show.html', context=context)


def tag_show(request, tag_slug):
    try:
        tag = Tag.objects.get(slug=tag_slug)
        posts = Tag.objects.get(slug=tag_slug).post_set.all()
    except Exception as e:
        tag = False
        posts = None
    context = {'tag': tag, 'tag_slug': tag_slug, 'posts': posts}
    return render(request, 'blog/tag_show.html', context=context)

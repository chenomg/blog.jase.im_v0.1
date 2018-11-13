from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.text import slugify
from blog.models import Category, Tag, Post, Comment, Page
from .forms import CommentForm
from markdown import markdown, Markdown
from markdown.extensions.toc import TocExtension
# from uuslug import slugify
import datetime

md = Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    TocExtension(slugify=slugify),
])


def index(request):
    query = request.GET.get('query')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query))
    else:
        posts = Post.objects.all().order_by('-created_time')
    for post in posts:
        post.excerpt = md.convert(post.excerpt)
    posts_per_page = 4
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
        'query': query,
    }
    return render(request, 'blog/index.html', context=context_dic)


def about(request):
    page = Page.objects.get(title_slug='about')
    page.views += 1
    page.save()
    page.content = md.convert(page.content)
    page.toc = md.toc
    context_dic = {'page': page}
    return render(request, 'blog/about.html', context=context_dic)


def post_detail(request, post_title_slug):
    post = get_object_or_404(Post, title_slug=post_title_slug)
    post.views = post.views + 1
    post.save()
    post.content = md.convert(post.content)
    # post.content = markdown(post.content, extensions=exts)
    post.toc = md.toc
    comments = Post.objects.get(title_slug=post_title_slug).comment_set.all()
    tags = post.tags.all().order_by('slug')
    context = {
        'post': post,
        'comments': comments,
        'tags': tags,
    }
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            comment = Comment.objects.create(
                name=name, content=content, email=email, post=post)
            context['form'] = form
            return render(request, 'blog/post_detail.html', context=context)
    else:
        form = CommentForm()
    context['form'] = form
    return render(request, 'blog/post_detail.html', context=context)


def comment_submit(request):
    print('...')
    post_title_slug = request.META.get('post_title_slug')
    post = get_object_or_404(Post, title_slug=post_title_slug)
    comments = post.comment_set.all()
    context = {
        'comments': comments,
        'form': CommentForm(),
    }
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            comment = Comment.objects.create(
                name=name, content=content, email=email, post=post)
            return render(request, 'blog/comments_form_update.html', context=context)
        else:
            context['form'] = form
    return render(request, 'blog/comments_form_update.html', context=context)


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
        for p in posts:
            p.content = md.convert(p.content)
    except Exception as e:
        tag = False
        posts = None
    context = {'tag': tag, 'tag_slug': tag_slug, 'posts': posts}
    return render(request, 'blog/tag_show.html', context=context)


def search(request):
    if request.method == 'POST':
        quert = request.POST['query']
    else:
        query = None
        results = None
    context = {'results': results, 'query': query}
    return render(request, 'blog/search.html', context=context)

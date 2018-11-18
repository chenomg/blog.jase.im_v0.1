from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from blog.models import Category, Tag, Post, Comment, Page, UserProfile
from registration.backends.simple.views import RegistrationView
from .forms import CommentForm, UserProfileForm, UserUpdateForm, MDEditorModelForm
from markdown import markdown, Markdown
from markdown.extensions.toc import TocExtension
# from uuslug import slugify
import datetime
import json

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
    post_title_slug = request.POST['post_title_slug']
    post = get_object_or_404(Post, title_slug=post_title_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        response_data = {
            'success': False,
            'name': form['name'],
            'content': form['content'],
        }
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            comment = Comment.objects.create(
                name=name, content=content, email=email, post=post)
            response_data['success'] = True
            response_data['name'] = name
            response_data['content'] = content
            print('提交成功,正在刷新')
        return HttpResponse(
            json.dumps(response_data), content_type='application/json')


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


@login_required
def register_profile(request):
    """
    用于展示目前登陆用户的信息,并且可以更新部分信息, 未完成
    """
    user = User.objects.get(username=request.user.username)
    userprofile = None if not UserProfile.objects.filter(
        user=user) else UserProfile.objects.get(user=user)
    userform = UserUpdateForm({
        'email': user.email,
        'website': userprofile.website
    })
    if request.method == 'POST':
        userform = UserUpdateForm(request.POST)
        if userform.is_valid():
            user.email = userform.cleaned_data['email']
            user.save()
        if not userprofile:
            userprofile = UserProfile(
                user=user,
                website=userform.cleaned_data['website'],
                picture=request.POST.get('picture'))
        else:
            userprofile.website = userform.cleaned_data['website']
            picture = request.FILES.get('avator')
            if picture:
                userprofile.picture = picture
        userprofile.save()
    context = {'user': user, 'userprofile': userprofile, 'userform': userform}
    return render(request, 'blog/register_profile.html', context=context)


@login_required
def myposts(request):
    pass


@login_required
def edit_post(request):
    pass


@login_required
def add_post(request):
    user = User.objects.get(username=request.user.username)
    post_form = MDEditorModelForm()
    context = {'post_form': post_form, 'user': user}
    if request.method == 'POST':
        form = MDEditorModelForm(request.POST)
        print(form)
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data['title']
            post.author = User.objects.get(username=request.user.username)
            post.content = form.cleaned_data['content']
            post.excerpt = form.cleaned_data['excerpt']
            post.category = Category.objects.get(
                name=form.cleaned_data['category'])
            post.save()
            post.tags = form.cleaned_data['tags']
            post.save()
    return render(request, 'blog/add_post.html', context=context)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""XML-RPC methods for metaWeblog API"""
from datetime import datetime
from xmlrpc.client import DateTime
from xmlrpc.client import Fault

from django.contrib.auth import authenticate as authen
from django.conf import settings
# from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import six
from django.utils import timezone
from django.utils.translation import gettext as _

from django_xmlrpc.decorators import xmlrpc_func

# from tagging.models import Tag

from blog.models import Post, Category, Tag
# from zinnia.managers import DRAFT, PUBLISHED
# from zinnia.models.author import Author
# from zinnia.models.category import Category
# from zinnia.models.entry import Entry
# from zinnia.settings import PROTOCOL


# http://docs.nucleuscms.org/blog/12#errorcodes
LOGIN_ERROR = 801
PERMISSION_DENIED = 803
PROTOCOL = 'https'
DOMAIN = 'jase.im'
BLOGNAME = 'Do It!'
BLOGID = '0'


def authenticate(username, password, permission=None):
    """
    Authenticate staff_user with permission.
    """
    author = authen(username=username, password=password)
    if not author:
        raise Fault(LOGIN_ERROR, _('Username or Password is incorrect.'))
    if not author.is_staff or not author.is_active:
        raise Fault(PERMISSION_DENIED, _('User account unavailable.'))
    if permission:
        if not author.has_perm(permission):
            raise Fault(PERMISSION_DENIED, _('User cannot %s.') % permission)
    return author


def blog_structure():
    """
    A blog structure.
    """
    return {'blogid': BLOGID,
            'blogName': BLOGNAME,
            'url': '{}://{}{}'.format(
                PROTOCOL, DOMAIN,
                reverse('blog:index'))
            }


def user_structure(user, site):
    """
    An user structure.
    """
    full_name = user.get_full_name().split()
    first_name = full_name[0]
    try:
        last_name = full_name[1]
    except IndexError:
        last_name = ''
    return {'userid': user.pk,
            'email': user.email,
            'nickname': user.get_username(),
            'lastname': last_name,
            'firstname': first_name,
            'url': '%s://%s%s' % (
                PROTOCOL, site.domain,
                user.get_absolute_url())}


def author_structure(user):
    """
    An author structure.
    """
    return {'user_id': user.pk,
            'user_login': user.get_username(),
            'display_name': user.__str__(),
            'user_email': user.email}


def category_structure(category):
    """
    A category structure.
    """
    return {  # 'description': category.name,
        'htmlUrl': '%s://%s%s' % (
            PROTOCOL, DOMAIN,
            reverse('blog:category')),
        # Useful Wordpress Extensions
        'categoryId': category.pk,
        # 'categoryDescription': category.description,
        'categoryName': category.name}


def tag_structure(tag):
    """
    A tag structure.
    """
    return {'tag_id': tag.pk,
            'name': tag.name,
            # 'count': tag.count,
            'slug': tag.slug,
            'html_url': '%s://%s%s' % (
                PROTOCOL, DOMAIN,
                reverse('blog:tag_show', args=[tag.slug])),
            }


def post_structure(entry):
    """
    A post structure with extensions.
    """
    author = entry.author
    return {'title': entry.title,
            'description': entry.content,
            'link': '%s://%s%s' % (PROTOCOL, DOMAIN,
                                   reverse('blog:post_detail', kwargs={'slug':entry.slug})),
            # Basic Extensions
            # 'permaLink': '%s://%s%s' % (PROTOCOL, site.domain,
                                        # entry.get_absolute_url()),
            'categories': entry.category,
            'dateCreated': DateTime(entry.created_time.isoformat()),
            'postid': entry.pk,
            # 'userid': author.get_username(),
            'userid': author.pk,
            # Useful Movable Type Extensions
            'mt_excerpt': entry.excerpt,
            # 'mt_allow_comments': int(entry.comment_enabled),
            # 'mt_allow_pings': (int(entry.pingback_enabled) or
                               # int(entry.trackback_enabled)),
            'mt_keywords': entry.tags,
            # Useful Wordpress Extensions
            'wp_author': author.username,
            'wp_author_id': author.pk,
            'wp_author_display_name': author.__str__(),
            'wp_slug': entry.slug,
            # 'sticky': entry.featured}
    }


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_users_blogs(apikey, username, password):
    """
    blogger.getUsersBlogs(api_key, username, password)
    => blog structure[]
    """
    authenticate(username, password)
    return [blog_structure()]


@xmlrpc_func(returns='struct', args=['string', 'string', 'string'])
def get_user_info(apikey, username, password):
    """
    blogger.getUserInfo(api_key, username, password)
    => user structure
    """
    user = authenticate(username, password)
    site = Site.objects.get_current()
    return user_structure(user, site)


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_authors(apikey, username, password):
    """
    wp.getAuthors(api_key, username, password)
    => author structure[]
    """
    authenticate(username, password)
    return [author_structure(author)
            for author in Author.objects.filter(is_staff=True)]


@xmlrpc_func(returns='boolean', args=['string', 'string',
                                      'string', 'string', 'string'])
def delete_post(apikey, post_id, username, password, publish):
    """
    blogger.deletePost(api_key, post_id, username, password, 'publish')
    => boolean
    """
    user = authenticate(username, password, 'zinnia.delete_entry')
    entry = Entry.objects.get(id=post_id, authors=user)
    entry.delete()
    return True


@xmlrpc_func(returns='struct', args=['string', 'string', 'string'])
def get_post(post_id, username, password):
    """
    metaWeblog.getPost(post_id, username, password)
    => post structure
    """
    user = authenticate(username, password)
    # site = Site.objects.get_current()
    return post_structure(Post.objects.filter(id=post_id)[0])


@xmlrpc_func(returns='struct[]',
             args=['string', 'string', 'string', 'integer'])
def get_recent_posts(blog_id, username, password, number):
    """
    metaWeblog.getRecentPosts(blog_id, username, password, number)
    => post structure[]
    """
    user = authenticate(username, password)
    site = Site.objects.get_current()
    return [post_structure(entry, site)
            for entry in Entry.objects.filter(authors=user)[:number]]


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_tags(blog_id, username, password):
    """
    wp.getTags(blog_id, username, password)
    => tag structure[]
    """
    authenticate(username, password)
    site = Site.objects.get_current()
    return [tag_structure(tag, site)
            for tag in Tag.objects.usage_for_queryset(
                Entry.published.all(), counts=True)]


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_categories(blog_id, username, password):
    """
    metaWeblog.getCategories(blog_id, username, password)
    => category structure[]
    """
    authenticate(username, password)
    categories = Category.objects.all()
    return [category_structure(category)
            for category in categories]


@xmlrpc_func(returns='string', args=['string', 'string', 'string', 'struct'])
def new_category(blog_id, username, password, category_struct):
    """
    wp.newCategory(blog_id, username, password, category)
    => category_id
    """
    authenticate(username, password, 'zinnia.add_category')
    category_dict = {'title': category_struct['name'],
                     'description': category_struct['description'],
                     'slug': category_struct['slug']}
    if int(category_struct['parent_id']):
        category_dict['parent'] = Category.objects.get(
            pk=category_struct['parent_id'])
    category = Category.objects.create(**category_dict)

    return category.pk


@xmlrpc_func(returns='string', args=['string', 'string', 'string',
                                     'struct', 'boolean'])
def new_post(blog_id, username, password, post, publish):
    """
    metaWeblog.newPost(blog_id, username, password, post, publish)
    => post_id
    """
    user = authenticate(username, password)
    creation_date = timezone.now()
    new_post = Post()
    new_post.title = post['title']
    new_post.content = post['description']
    new_post.excerpt = post['description'][:300]
    new_post.author = user
    new_post.is_publish = True if post['post_status']=='publish' else False
    if new_post.is_publish:
        new_post.publish_content = new_post.content
        new_post.publish_excerpt = new_post.excerpt
    if 'categories' in post and post['categories']:
        # 文章的类别只选择第一项
        cat = post['categories'][0]
        new_post.category = Category.objects.get(name=cat)
    else:
        new_post.category, _ = Category.objects.get_or_create(name='未分类')
    new_post.save()
    # new_post.publish_excerpt = post['mt_excerpt']
    if 'mt_keywords' in post and post['mt_keywords']:
        ts = [i.strip() for i in post['mt_keywords'].split(',')]
        for t in ts:
            tag, _ = Tag.objects.get_or_create(name=t)
            new_post.tags.add(tag)
    return new_post.pk


@xmlrpc_func(returns='boolean', args=['string', 'string', 'string',
                                      'struct', 'boolean'])
def edit_post(post_id, username, password, post, publish):
    """
    metaWeblog.editPost(post_id, username, password, post, publish)
    => boolean
    """
    user = authenticate(username, password)
    post = Post.objects.get(id=post_id, authors=user)
    if 'wp_author_id' in post:
        if int(post['wp_author_id']) != user.pk:
            return False

    post.title = post['title']
    post.content = post['description']
    post.excerpt = post.get('mt_excerpt', '')
    # entry.comment_enabled = post.get('mt_allow_comments', 1) == 1
    # entry.pingback_enabled = post.get('mt_allow_pings', 1) == 1
    # entry.trackback_enabled = post.get('mt_allow_pings', 1) == 1
    # entry.featured = post.get('sticky', 0) == 1
    post.is_publish = True if post['post_status']=='publish' else False
    if post.is_publish:
        post.publish_content = post.content
        post.publish_excerpt = post.excerpt
    if 'categories' in post and post['categories']:
        # 文章的类别只选择第一项
        cat = post['categories'][0]
        post.category = Category.objects.get(name=cat)
    else:
        post.category, _ = Category.objects.get_or_create(name='未分类')
    post.save()
    # new_post.publish_excerpt = post['mt_excerpt']
    if 'mt_keywords' in post and post['mt_keywords']:
        ts = [i.strip() for i in post['mt_keywords'].split(',')]
        for t in ts:
            tag, _ = Tag.objects.get_or_create(name=t)
            post.tags.add(tag)
    # entry.tags = 'mt_keywords' in post and post['mt_keywords'] or ''
    # entry.slug = 'wp_slug' in post and post['wp_slug'] or slugify(
        # post['title'])
    # if user.has_perm('zinnia.can_change_status'):
        # entry.status = publish and PUBLISHED or DRAFT
    # entry.password = post.get('wp_password', '')
    # entry.save()


    # if 'categories' in post:
        # entry.categories.clear()
        # entry.categories.add(*[
            # Category.objects.get_or_create(
                # title=cat, slug=slugify(cat))[0]
            # for cat in post['categories']])
    return True


@xmlrpc_func(returns='struct', args=['string', 'string', 'string', 'struct'])
def new_media_object(blog_id, username, password, media):
    """
    metaWeblog.newMediaObject(blog_id, username, password, media)
    => media structure
    """
    # authenticate(username, password)
    # path = default_storage.save(Entry().image_upload_to(media['name']),
    #                             ContentFile(media['bits'].data))
    return {'msg': '不支持图片上传，请使用图片链接'}

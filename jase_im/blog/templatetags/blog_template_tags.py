#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import template
from blog.models import Category, Post, Tag
import math

register = template.Library()
NAME_LEN_SIDEBAR = 35


@register.inclusion_tag('blog/show_current_categories.html')
def show_current_categories(is_detail=False, post=None):
    if is_detail:
        categories = post.category
    else:
        categories = Category.objects.all()
        pre_half = categories[:math.ceil(categories.count() / 2)]
        lst_half = categories[math.ceil(categories.count() / 2):]
    return {
        'categories': categories,
        'pre_half': pre_half,
        'lst_half': lst_half,
        'is_detail': is_detail
    }


@register.inclusion_tag('blog/show_current_tags.html')
def show_current_tags(is_detail=False, post=None):
    if is_detail:
        tags = post.tags.all()
    else:
        tags = Tag.objects.all()
        pre_half = tags[:math.ceil(tags.count() / 2)]
        lst_half = tags[math.ceil(tags.count() / 2):]
    return {
        'tags': tags,
        'pre_half': pre_half,
        'lst_half': lst_half,
    }


@register.inclusion_tag('blog/most_viewed_posts.html')
def most_viewed_posts():
    posts = Post.objects.order_by('-views')[:5]
    for p in posts:
        if len(p.title) > NAME_LEN_SIDEBAR:
            p.sidebar_name = p.title[:NAME_LEN_SIDEBAR] + '...'
        else:
            p.sidebar_name = p.title[:NAME_LEN_SIDEBAR]
    return {'most_viewed_posts': posts}


@register.inclusion_tag('blog/recent_posts.html')
def recent_posts():
    posts = Post.objects.order_by('-modified_time')[:5]
    for p in posts:
        if len(p.title) > NAME_LEN_SIDEBAR:
            p.sidebar_name = p.title[:NAME_LEN_SIDEBAR] + '...'
        else:
            p.sidebar_name = p.title[:NAME_LEN_SIDEBAR]
    return {'recent_posts': posts}

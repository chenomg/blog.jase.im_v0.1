#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import template
from blog.models import Category, Post, Tag

register = template.Library()


@register.inclusion_tag('blog/show_current_categories.html')
def show_current_categories(posts):
    categories = None
    if len(posts) == 1:
        categories = posts.categroy
    elif len(posts) > 1:
        categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('blog/show_current_tags.html')
def show_current_tags(posts):
    tags = None
    if len(posts) > 1:
        tags = Tag.objects.all()
    elif len(posts) == 1:
        tags = posts.tags.all()
    return {'tags': tags}


@register.inclusion_tag('blog/most_viewed_posts.html')
def most_viewed_posts():
    return {'most_viewed_posts': Post.objects.order_by('-views')[:5]}


@register.inclusion_tag('blog/recent_posts.html')
def recent_posts():
    return {'recent_posts': Post.objects.order_by('-modified_time')[:5]}

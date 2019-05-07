from django.contrib import admin
from blog.models import Category, Tag, Post, Page, Comment, UserProfile
import xadmin


class CategoryAdmin(object):
    fields = ['name']
    # inlines = [PostInline]
    list_display = ('name', 'created_time', 'slug')


class TagAdmin(object):
    fields = ['name']
    list_display = ('name', 'created_time', 'slug')


class PostAdmin(object):
    fields = [
        'title',
        'content',
        'excerpt',
        'category',
        'views',
        'author',
        'tags',
        'is_publish',
    ]
    list_display = ('title', 'created_time', 'category', 'views', 'author',
                    'slug', 'is_publish')


class PageAdmin(object):
    fields = [
        'title',
        'content',
        'views',
    ]
    list_display = ('title', 'created_time', 'views', 'slug')


class CommentAdmin(object):
    fields = ['name', 'email', 'post', 'content']
    list_display = ('name', 'email', 'created_time', 'post', 'content')


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Page, PageAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(UserProfile)

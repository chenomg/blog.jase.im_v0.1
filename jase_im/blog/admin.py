from django.contrib import admin
from blog.models import Category, Tag, Post, Page


class PostInline(admin.TabularInline):
    model = Post
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    # inlines = [PostInline]
    list_display = ('name', 'created_time', 'slug')


class TagAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name', 'created_time', 'slug')


class PostAdmin(admin.ModelAdmin):
    fields = [
        'title', 'content', 'excerpt', 'category', 'views', 'author', 'tags'
    ]
    list_display = ('title', 'created_time', 'category', 'views', 'author',
                    'title_slug')


class PageAdmin(admin.ModelAdmin):
    fields = [
        'title', 'content', 'views',
    ]
    list_display = ('title', 'created_time', 'views', 'title_slug')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)

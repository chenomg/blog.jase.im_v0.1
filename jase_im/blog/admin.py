from django.contrib import admin
from blog.models import Category, Tag, Post, Archive


class PostInline(admin.TabularInline):
    model = Post
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    inlines = [PostInline]
    list_display = ('name', 'created_time')


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'excerpt', 'category', 'views']
    list_display = ('title', 'created_time', 'content', 'category', 'views')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Archive)

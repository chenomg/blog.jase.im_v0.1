from django.db import models
from django.contrib.auth.models import User
from uuslug import slugify
from mdeditor.fields import MDTextField
from random import choice
from datetime import datetime


def gene_rand_code(digital=8):
    S = [chr(i) for i in range(48, 58)]
    S += [chr(i) for i in range(97, 123)]
    S += [chr(i) for i in range(65, 91)]
    res = []
    for i in range(digital):
        res.append(choice(S))
    return ''.join(res)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'tags'


class Post(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(default=datetime.now)
    # content = models.TextField()
    publish_content = MDTextField()
    publish_excerpt = MDTextField(blank=True)
    content = MDTextField()
    excerpt = MDTextField(blank=True)
    # excerpt = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField()
    views = models.PositiveIntegerField(default=0)
    is_publish = models.BooleanField(default=False)

    # likes = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            rcd = gene_rand_code()
            slg_t = slugify(self.title) + '-' + rcd
            while Post.objects.filter(slug=slg_t):
                rcd = gene_rand_code()
            self.slug = slg_t
        if not self.excerpt:
            if len(self.content) < 301:
                self.excerpt = self.content[:300]
            else:
                self.excerpt = self.content[:300] + '...'
        if not self.author:
            self.author = 'Unknow Author'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'posts'


class Page(models.Model):
    """
    用于网站相关页面的显示, 如about, 404等
    """
    title = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    content = MDTextField()
    slug = models.SlugField(blank=True)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'pages'


class Comment(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post)

    def __str__(self):
        return self.content


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Vistor(models.Model):
    """
    记录网站来访者信息,暂未使用
    """
    ip = models.GenericIPAddressField()
    agent = models.TextField()
    visit_time = models.TimeField()
    visitor_position = models.TextField()

    def __str__(self):
        return self.ip

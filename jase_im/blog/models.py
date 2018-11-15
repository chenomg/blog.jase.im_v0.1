from django.db import models
from uuslug import slugify
from mdeditor.fields import MDTextField


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
    author = models.CharField(max_length=128, default='Jase Chen')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # content = models.TextField()
    content = MDTextField()
    excerpt = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    title_slug = models.SlugField(blank=True)
    views = models.PositiveIntegerField(default=0)
    # likes = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        if not self.excerpt:
            if len(self.content) <201:
                self.excerpt = self.content[:200]
            else:
                self.excerpt = self.content[:200] + '...'
        if not self.author:
            self.author = 'Unknow Author'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'posts'


class Page(models.Model):
    title = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    content = MDTextField()
    title_slug = models.SlugField(blank=True)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
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

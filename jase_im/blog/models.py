from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'tags'


class Page(models.Model):
    title = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    tag = models.ManyToManyField(Tag)
    title_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __repr__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'pages'


class Archive(models.Model):
    pass

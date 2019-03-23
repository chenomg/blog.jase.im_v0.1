from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from uuslug import slugify
from blog.models import gene_rand_code

# Create your models here.


def user_file_path(instance, filename):
    return "api/file/{}".format(filename)


def user_image_path(instance, filename):
    return "api/image/{}".format(filename)
    # return "user_{}/image/{}".format(instance.user.username, filename)


class FileHostingModel(models.Model):
    title = models.CharField(max_length=32, blank=False)
    slug = models.CharField(unique=True, max_length=64, blank=True)
    created_time = models.DateField(auto_now_add=True)
    file_upload = models.FileField(upload_to=user_file_path)


class ImageHostingModel(models.Model):
    title = models.CharField(max_length=32, blank=False)
    slug = models.CharField(unique=True, max_length=64, blank=True)
    format = models.CharField(max_length=32, default='jpeg')
    user = models.ForeignKey(User, null=True)
    created_time = models.DateField(auto_now_add=True)
    image_upload = models.ImageField(upload_to=user_image_path)

    def save(self, *args, **kwargs):
        if not self.slug:
            rcd = gene_rand_code()
            slg_t = slugify(self.title) + '-' + rcd
            while ImageHostingModel.objects.filter(slug=slg_t):
                rcd = gene_rand_code()
                slg_t = slugify(self.title) + '-' + rcd
            self.slug = slg_t
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserType(models.Model):
    ADMIN = 0
    NORMAL = 1
    USER_TYPE = [(ADMIN, 'Admin'), (NORMAL, 'Normal')]
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=USER_TYPE, default=NORMAL)

    def __str__(self):
        return type, self.user.username
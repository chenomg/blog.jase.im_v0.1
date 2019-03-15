from django.db import models

# Create your models here.

def user_file_path(instance, filename):
    return "user_{}/file/{}".format(instance.user.username, filename)

def user_image_path(instance, filename):
    return "user_{}/image/{}".format(instance.user.username, filename)

class FileHostingModel(models.Model):
    title = models.CharField(max_length=50, blank=False)
    title_slug = models.CharField(max_length=100)
    created_time = models.DateField(auto_now_add=True)
    upload = models.FileField(upload_to=user_file_path)

class ImageHostingModel(models.Model):
    title = models.CharField(max_length=50, blank=False)
    title_slug = models.CharField(max_length=100)
    created_time = models.DateField(auto_now_add=True)
    upload = models.ImageField(upload_to=user_image_path)

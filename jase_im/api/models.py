from django.db import models
from uuslug import slugify
from blog.models import gene_rand_code

# Create your models here.

def user_file_path(instance, filename):
    return "user_{}/file/{}".format(instance.user.username, filename)

def user_image_path(instance, filename):
    return "user_{}/image/{}".format(instance.user.username, filename)

class FileBaseModel(models.Model):
    title = models.CharField(max_length=32, blank=False)
    slug = models.CharField(unique=True, max_length=64)
    created_time = models.DateField(auto_now_add=True)

class FileHostingModel(FileBaseModel):
    upload = models.FileField(upload_to=user_file_path)

class ImageHostingModel(FileBaseModel):
    upload = models.ImageField(upload_to=user_image_path)

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


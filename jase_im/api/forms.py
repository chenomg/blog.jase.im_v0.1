# 未使用
from django.forms import ModelForm
from api.models import ImageHostingModel

class UploagImageForm(ModelForm):
    class Meta:
        model = ImageHostingModel
        fields = ['title']
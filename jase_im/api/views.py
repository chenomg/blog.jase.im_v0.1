import json
import os

import requests
# from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from jase_im.settings import MEDIA_ROOT
from api.models import ImageHostingModel
from api.utils.serializers import ImageGetSerializer
from api.utils.url import get_image_url
# Create your views here.


class Bing_Daily_Wallpaper(APIView):
    def get(self, request, version, format=None):
        request_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
        base_url = 'http://s.cn.bing.net'
        res = requests.get(request_url)
        data = json.loads(res.text)
        img_url = base_url + data['images'][0]['url']
        response = requests.get(img_url)
        return HttpResponse(response.content, content_type='image/jpeg')


class ImageView(APIView):
    """
    用于图床的上传及查看
    """
    ret = {
        "code": 1001,  # 业务自定义状态码
        "msg": '',  # 请求状态描述，调试用
        "data": {},  # 请求数据，对象或数组均可
        "extra": {},  # 全局附加数据，字段、内容不定
    }

    def get_object(self, slug):
        try:
            return ImageHostingModel.objects.get(slug=slug)
        except ImageHostingModel.DoesNotExist:
            raise Http404
    
    def get(self, request, version, slug=None):
        if slug is not None:
            img = self.get_object(slug)
            image_open = open(
                os.path.join(MEDIA_ROOT, str(img.image_upload)),
                'rb').read()
            return HttpResponse(image_open, content_type='image/jpeg')
        else:
            imgs = ImageHostingModel.objects.all()
            serializer = ImageGetSerializer(imgs, many=True)
            return Response(serializer.data)

    def post(self, request, version):
        new_img = request.FILES.get('image')
        if new_img:
            print('new image post')
            instance = ImageHostingModel(
                title=str(request.FILES.get('image')), image_upload=new_img)
            print('new image')
            instance.save()
            self.ret['code'] = 1001
            self.ret['msg'] = '图片上传成功'
            self.ret['data']['url'] = self.get_image_url(instance)
        else:
            self.ret['code'] = 2001
            self.ret['msg'] = '图片上传失败'
        return Response(data=self.ret, status=status.HTTP_201_CREATED)

    def delete(self, request, version, slug=None):
        img = self.get_object(slug)
        img.delete()
        self.ret['code'] = 3001
        self.ret['msg'] = '图片删除成功'
        self.ret['data'] = {}
        return Response(data=self.ret, status=status.HTTP_204_NO_CONTENT)

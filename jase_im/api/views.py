import json

# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.


class Bing_Daily_Wallpaper(APIView):
    def get(self, request, format=None):
        request_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
        base_url = 'http://s.cn.bing.net'
        res = requests.get(request_url)
        data = json.loads(res.content)
        img_url = base_url + data['images'][0]['url']
        return redirect(img_url)


class ImageView(APIView):
    def get(self, request, format=None):
        return HttpResponse('Image GET success!')

    def post(self, request, format=None):
        img = request.FILES.get('image', '未上传成功')
        with open('media/api/{}'.format(img), 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
        return HttpResponse('Image:{} Post success!'.format(img))

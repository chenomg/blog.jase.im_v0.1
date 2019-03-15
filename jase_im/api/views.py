import json

# from django.shortcuts import render
from django.http import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.


class Bing_Daily_Wallpaper(viewsets.ViewSet):
    def get(self, request, format=None):
        request_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
        base_url = 'http://s.cn.bing.net'
        res = requests.get(request_url)
        data = json.loads(res.content)
        img_url = base_url + data['images'][0]['url']
        return Response(img_url)


class ImageView(APIView):
    def get(self, request, format=None):
        return HttpResponse('post success!')

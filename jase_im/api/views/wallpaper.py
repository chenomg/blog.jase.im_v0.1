import json

import requests
from django.http import HttpResponse, Http404
from rest_framework.views import APIView


class Bing_Daily_Wallpaper(APIView):
    def get(self, request, version, format=None):
        request_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
        base_url = 'http://s.cn.bing.net'
        res = requests.get(request_url)
        data = json.loads(res.text)
        img_url = base_url + data['images'][0]['url']
        response = requests.get(img_url)
        return HttpResponse(response.content, content_type='image/jpeg')

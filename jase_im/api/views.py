# from django.shortcuts import render
import requests
import json

# Create your views here.


def bing_daily_wallpaper():
    request_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
    base_url = 'http://s.cn.bing.net'
    res = requests.get(request_url)
    data = json.loads(res.content)
    img_url = base_url + data['images'][0]['url']
    return img_url


if __name__ == "__main__":
    r = bing_daily_wallpaper()
    print(r)

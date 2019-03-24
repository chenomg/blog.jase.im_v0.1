import json
import os

import requests
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.settings import api_settings
from rest_framework.settings import DEFAULTS

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
    用于图片的上传及查看
    """
    DEFAULTS['IMAGE_TYPES'] = ('jpg', 'jpeg', 'png', 'bmp', 'gif', 'icon')
    image_types = api_settings.IMAGE_TYPES

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
            return HttpResponse(image_open, content_type='image/{}'.format(img.format))
        else:
            ret = {
                "code": 1001,  # 业务自定义状态码
                "msg": None, # 请求状态描述，调试用
                "data": {},  # 请求数据，对象或数组均可
                # "extra": {},  # 全局附加数据，字段、内容不定
            }
            if isinstance(request.user, AnonymousUser):
                ret['msg'] = '未认证用户无法获取图片列表'
                return Response(ret)
            imgs = ImageHostingModel.objects.filter(user=request.user)
            serializer = ImageGetSerializer(imgs, many=True)
            ret['msg'] = 'user：{} 的图片清单获取成功'.format(request.user)
            ret['data']['total'] = len(imgs)
            ret['data']['list'] = serializer.data
            return Response(ret)

    def post(self, request, version):
        ret = {
            "code": 2001,  # 业务自定义状态码
            "msg": '图片上传失败', # 请求状态描述，调试用
        }
        new_img = request.FILES.get('image')
        if new_img:
            title=str(request.FILES.get('image'))
            if '.' in title[1:]:
                ext = title.split('.')[-1]
                if ext.lower() in self.image_types:
                    instance = ImageHostingModel(
                        title=title, user=request.user, format=ext.lower(), image_upload=new_img)
                    instance.save()
                    ret = {
                        "code": 1001,  # 业务自定义状态码
                        "msg": '图片上传成功', # 请求状态描述，调试用
                        "data": {'url': get_image_url(instance)},  # 请求数据，对象或数组均可
                    }
                else:
                    ret['msg'] = '图片上传失败，图片类型不支持'
                    return Response(ret)
            else:
                ret['msg'] = '图片上传失败，请检查文件名'
                return Response(ret)
        return Response(data=ret)

    def delete(self, request, version, slug=None):
        img = self.get_object(slug)
        if img.user != request.user:
            raise PermissionDenied('抱歉，无权限进行此操作')
        img.delete()
        ret = {
            "code": 3001,  # 业务自定义状态码
            "msg": '图片删除成功', # 请求状态描述，调试用
        }
        return Response(data=ret)

class Auth(APIView):
    """
    使用用户名及密码获取或更新用户token
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def auth(self, request):
        ret = {
            "code": 1001,  # 业务自定义状态码
            "msg": None, # 请求状态描述，调试用
            "data": {},  # 请求数据，对象或数组均可
            "extra": {},  # 全局附加数据，字段、内容不定
        }
        try:
            username = request._request.POST.get('username')
            password = request._request.POST.get('password')
            user = authenticate(username=username, password=password)
            if not user:
                ret['code'] = 2002
                ret['msg'] = '用户名或密码错误'
                return (None, None, ret)
            ret['code'] = 1002
            ret['msg'] = '用户认证成功'
            token = Token.objects.filter(user=user).first()
            if not token:
                token = Token.objects.create(user=user)
                ret['extra'] = '首次登陆及生成令牌'
            ret['data']['token'] = token.key
            return (user, token, ret)
        except Exception as e:
            ret['code'] = 2003
            ret['msg'] = '登陆请求异常'
        return (None, None, ret)


    def get(self, request, version):
        return Response({
            "code": 2001,  # 业务自定义状态码
            "msg": '方法请求失败,请使用POST', # 请求状态描述，调试用
        })

    def post(self, request, version):
        """
        提交用户名及密码查看token
        form-data中添加：_token_to_do: update, 则更新token并返回
        """
        user, token, ret = self.auth(request)
        _token_to_do = request._request.POST.get('token_to_do')
        # print(_token_to_do)
        if _token_to_do:
            if _token_to_do.lower() == 'update':
                token.delete()
                token = Token.objects.create(user=user)
                ret['data']['token'] = token.key
                ret['extra'] = '令牌已更新'
        return Response(ret)


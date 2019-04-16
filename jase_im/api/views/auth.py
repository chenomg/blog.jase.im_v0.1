from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class Auth(APIView):
    """
    使用用户名及密码获取或更新用户token
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def auth(self, request):
        ret = {
            "code": 1001,  # 业务自定义状态码
            "msg": None,  # 请求状态描述，调试用
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
            "msg": '方法请求失败,请使用POST',  # 请求状态描述，调试用
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

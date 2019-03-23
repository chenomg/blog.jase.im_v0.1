from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
# from blog.models import UserToken


class TokenAuthentication(BaseAuthentication):
    """
    在HEADER字段中添加token：key
    """
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        token_obj = Token.objects.filter(key=token).first()
        if not token_obj:
            raise AuthenticationFailed('用户认证失败！')
        return (token_obj.user, token_obj)

    # def authenticate_header(self, request):
    #     pass

class AnonymousOrTokenAuthentication(BaseAuthentication):
    """
    在HEADER字段中添加token：key将使用认证，否则为匿名
    """
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if token:
            token_obj = Token.objects.filter(key=token).first()
            if not token_obj:
                raise AuthenticationFailed('用户认证失败！')
            return (token_obj.user, token_obj)
        else:
            return None

    # def authenticate_header(self, request):
    #     pass

from rest_framework.throttling import SimpleRateThrottle
from django.contrib.auth.models import AnonymousUser

class AnonymousThrottle(SimpleRateThrottle):
    """
    匿名用户一分钟限制访问api次数
    """
    scope = "AnonymousUser"

    # def allow_request(self, request, view):
    #     if not isinstance(request.user, AnonymousUser):
    #         return True
    #     else:
    #         super().allow_request(request, view)

    def get_cache_key(self, request, view):
        # 通过ip限制节流
        return self.get_ident(request)

class NormalThrottle(SimpleRateThrottle):
    """
    普通登录用户一分钟限制访问api次数
    """
    scope = "NormalUser"

    # def allow_request(self, request, view):
    #     if isinstance(request.user, AnonymousUser):
    #         return True
    #     else:
    #         super().allow_request(request, view)

    def get_cache_key(self, request, view):
        # 通过ip限制节流
        return request.user.username

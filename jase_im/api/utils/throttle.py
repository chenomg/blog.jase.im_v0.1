from rest_framework.throttling import SimpleRateThrottle

class AnonymousThrottle(SimpleRateThrottle):
    """
    匿名用户一分钟限制访问api次数
    """
    scope = "AnonymousUser"

    def get_cache_key(self, request, view):
        # 通过ip限制节流
        return self.get_ident(request)

class NormalThrottle(SimpleRateThrottle):
    """
    普通登录用户一分钟限制访问api次数
    """
    scope = "NormalUser"

    def get_cache_key(self, request, view):
        # 通过ip限制节流
        return request.user.username

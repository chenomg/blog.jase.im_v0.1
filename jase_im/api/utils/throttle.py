from rest_framework.throttling import SimpleRateThrottle
from django.contrib.auth.models import AnonymousUser


class AnonRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a anonymous users.

    The IP address of the request will be used as the unique cache key.
    """
    scope = 'AnonymousUser'

    def get_cache_key(self, request, view):
        # if request.user.is_authenticated:
        if not isinstance(request.user, AnonymousUser):
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

class UserRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user.

    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    scope = 'NormalUser'

    def get_cache_key(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return None
        else:
            ident = request.user.pk

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


import json

import requests
from django.http import HttpResponse, Http404
from rest_framework.views import APIView

from blog.views import get_remote_ip

class Request_IPv4(APIView):
    def get(self, request, version, format=None):
        return HttpResponse(get_remote_ip(request), content_type='plain/txt')

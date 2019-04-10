from rest_framework.views import APIView
from rest_framework.response import Response


class Parser(APIView):
    # permission_classes = [AllowAny]
    def post(self, request, version):
        return Response(request.data)

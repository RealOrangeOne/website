from django.http.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView


class PingAPIView(APIView):
    """
    PONGs
    """

    def get(self, request: HttpRequest) -> Response:
        return Response("PONG")

from urllib import response
from rest_framework import views, status
from rest_framework.response import Response

from .serializer import ChannelUrlSerializer 

class ChannelUrlApiView(views.APIView):

    def post(self, request):
        serializer = ChannelUrlSerializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_201_CREATED)
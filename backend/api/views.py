from pprint import pprint

from rest_framework import views, status
from rest_framework.response import Response

from .serializer import ChannelUrlSerializer
from .random_videos import main

class ChannelUrlApiView(views.APIView):

    def post(self, request):
        print(request.data)
        serializer = ChannelUrlSerializer(data=request.data)
        serializer.is_valid()
        url = serializer.data
        videos = main(url['url'])
        return Response(videos, status.HTTP_201_CREATED)
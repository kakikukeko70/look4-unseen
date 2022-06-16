from pyexpat import model
from rest_framework import serializers
from .models import Channel


class ChannelUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ['url']
from unicodedata import name
from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Video(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
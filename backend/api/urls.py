from django.urls import path, include

from . import views

urlpatterns = [
    path('channel_url/', views.ChannelUrlApiView.as_view()),
]
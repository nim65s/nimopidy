from django.conf.urls import url

from .views import playlists, snapcast, webhooks

app_name = 'musicapp'
urlpatterns = [
    url(r'^webhooks', webhooks, name='webhooks'),
    url(r'^snapcast$', snapcast, name='snapcast'),
    url(r'^playlists$', playlists, name='playlists'),
]

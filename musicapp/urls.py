from django.conf.urls import url

from .views import TrackUpdateView, playlists, snapcast, webhooks

app_name = 'musicapp'
urlpatterns = [
    url(r'^webhooks', webhooks, name='webhooks'),
    url(r'^snapcast$', snapcast, name='snapcast'),
    url(r'^playlists$', playlists, name='playlists'),
    url(r'^track/(?P<slug>[^/]*)', TrackUpdateView.as_view(), name='track'),
]

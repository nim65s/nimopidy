from django.conf.urls import url

from .views import TrackUpdateView, playlists, snapcast, start_view, webhooks

app_name = 'musicapp'
urlpatterns = [
    url(r'^start', start_view, name='webhooks'),
    url(r'^webhooks', webhooks, name='webhooks'),
    url(r'^snapcast$', snapcast, name='snapcast'),
    url(r'^playlists$', playlists, name='playlists'),
    url(r'^track/(?P<slug>[^/]*)', TrackUpdateView.as_view(), name='track'),
]

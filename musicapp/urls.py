from django.urls import path

from .views import TrackUpdateView, playlists, snapcast, start_view, webhooks

app_name = 'musicapp'
urlpatterns = [
    path('start', start_view, name='webhooks'),
    path('webhooks', webhooks, name='webhooks'),
    path('snapcast', snapcast, name='snapcast'),
    path('playlists', playlists, name='playlists'),
    path('track/<str:slug>', TrackUpdateView.as_view(), name='track'),
]

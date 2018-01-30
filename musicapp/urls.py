from django.urls import path

from . import views

app_name = 'musicapp'
urlpatterns = [
    path('start', views.start_view, name='webhooks'),
    path('webhooks', views.webhooks, name='webhooks'),
    path('snapcast', views.snapcast, name='snapcast'),
    path('playlists', views.playlists, name='playlists'),
    path('track/<str:slug>', views.TrackUpdateView.as_view(), name='track'),
    path('track/<int:tlid>/del', views.remove_track, name='del-track'),
]

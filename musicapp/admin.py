from django.contrib.admin import site

from .models import Album, Artist, Playlist, PlaylistTrack, Track

site.register(Track)
site.register(Album)
site.register(Artist)
site.register(Playlist)
site.register(PlaylistTrack)

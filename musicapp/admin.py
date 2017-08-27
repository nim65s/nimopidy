from django.contrib.admin import site

from .models import Album, Artist, Playlist, Track

site.register(Track)
site.register(Album)
site.register(Artist)
site.register(Playlist)

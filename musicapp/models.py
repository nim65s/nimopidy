from io import BytesIO

from django.core import files
from django.db import models

import requests

from .utils import get_lyrics, mopidy_api


class NamedModel(models.Model):
    name = models.CharField(max_length=200)
    uri = models.CharField(max_length=200, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Artist(NamedModel):
    pass


class Album(NamedModel):
    artists = models.ManyToManyField(Artist, blank=True)
    date = models.PositiveSmallIntegerField(blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    def get_cover(self):
        cover_url = mopidy_api('core.library.get_images', uris=[self.uri])[self.uri][1]['uri']

        fp = BytesIO()
        fp.write(requests.get(cover_url).content)
        self.cover.save(self.uri, files.File(fp))
        self.save()


class Track(NamedModel):
    artists = models.ManyToManyField(Artist, blank=True)
    date = models.PositiveSmallIntegerField(blank=True, null=True)
    album = models.ForeignKey(Album, blank=True, null=True, related_name='songs')
    lyrics = models.TextField(null=True, default=None)
    length = models.PositiveIntegerField()
    disc_no = models.PositiveSmallIntegerField(default=0)
    track_no = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['date', 'album__name', 'disc_no', 'track_no', 'name']

    def get_lyrics(self):
        self.lyrics = get_lyrics(self.artists.first(), self.name)
        self.save()

    def json(self):
        return {
            'name': self.name, 'album': self.album.name or '', 'lyrics': self.lyrics, 'uri': self.uri,
            'length': self.length, 'artists': ', '.join(artist.name for artist in self.artists.all()),
            'cover': self.album.cover.url or '',
        }


class Playlist(NamedModel):
    active = models.BooleanField(default=False)

    @classmethod
    def update(cls):
        for playlist in mopidy_api('core.playlists.get_playlists', include_tracks=False):
            Playlist.objects.get_or_create(uri=playlist['uri'], defaults={'name': playlist['name']})

    def json(self):
        return {'name': self.name, 'uri': self.uri, 'active': self.active}

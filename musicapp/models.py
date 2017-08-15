from django.db import models

from .utils import get_lyrics


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
            'name': self.name, 'album': self.album.name, 'lyrics': self.lyrics, 'uri': self.uri, 'length': self.length,
            'artists': ', '.join(artist.name for artist in self.artists.all()), 'cover': self.album.cover or '',
        }

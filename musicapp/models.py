from django.db import models

from .utils import get_lyrics


class Song(models.Model):
    uri = models.CharField(max_length=200, unique=True)
    lyrics = models.TextField(null=True, default=None)
    artist = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def get_absolute_url(self):
        return '/'

    def get_lyrics(self):
        self.lyrics = get_lyrics(self.artist, self.title)
        self.save()

    def json(self):
        # TODO improve this
        return {'uri': self.uri, 'lyrics': self.lyrics, 'artist': self.artist, 'title': self.title}

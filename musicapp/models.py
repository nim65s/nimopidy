from django.db import models

from .utils import get_lyrics


class Song(models.Model):
    uri = models.CharField(max_length=200, unique=True)
    lyrics = models.TextField(null=True, default=None)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def get_lyrics(self):
        if self.lyrics is not None:
            return self.lyrics
        self.lyrics = get_lyrics(self.artist, self.title)
        self.save()
        return self.lyrics

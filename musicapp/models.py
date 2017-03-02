from django.db import models

from .utils import get_lyrics


class Song(models.Model):
    uri = models.CharField(max_length=200, unique=True)
    lyrics = models.TextField(null=True, default=None)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def save(self, *args, **kwargs):
        if self.lyrics is None:
            self.lyrics = get_lyrics(self.artist, self.title)
        super().save(*args, **kwargs)

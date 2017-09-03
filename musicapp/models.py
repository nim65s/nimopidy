from datetime import timedelta
from io import BytesIO

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core import files
from django.db import models
from django.utils import timezone

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
        try:
            cover_url = mopidy_api('core.library.get_images', uris=[self.uri])[self.uri][1]['uri']

            fp = BytesIO()
            fp.write(requests.get(cover_url).content)
            self.cover.save(self.uri, files.File(fp))
            self.save()
        except:
            print(f"Can't get cover for {self}")


class Track(NamedModel):
    artists = models.ManyToManyField(Artist, blank=True)
    date = models.PositiveSmallIntegerField(blank=True, null=True)
    album = models.ForeignKey(Album, blank=True, null=True, related_name='songs')
    lyrics = models.TextField(null=True, default=None)
    length = models.PositiveIntegerField(null=True)
    disc_no = models.PositiveSmallIntegerField(default=0)
    track_no = models.PositiveSmallIntegerField(default=0)
    playcount = models.PositiveIntegerField(default=0)
    last_play = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['date', 'album__name', 'disc_no', 'track_no', 'name']

    def get_lyrics(self):
        self.lyrics = get_lyrics(self.artists.first(), self.name)
        self.save()

    def json(self):
        return {
            'name': self.name, 'album': self.album.name if self.album else '', 'lyrics': self.lyrics, 'uri': self.uri,
            'length': self.length, 'artists': ', '.join(artist.name for artist in self.artists.all()),
            'cover': self.album.cover.url if self.album and self.album.cover else '', 'playcount': self.playcount,
            'last_play': naturaltime(self.last_play),
        }

    def update_from_mopidy(self):
        self.get_or_create_from_mopidy(uri=self.uri, force_update=True)

    @classmethod
    def get_or_create_from_mopidy(cls, track_data=None, uri='', force_update=False):
        if track_data is None:
            track_data = mopidy_api('core.library.lookup', uri=uri)[0]

        def get_or_create(model, data):
            keys = ['name', 'date', 'length', 'disc_no', 'track_no']
            if 'uri' not in data and data['name'] == 'YouTube':
                data['uri'] = 'youtube:dumb_album'
            return model.objects.get_or_create(uri=data['uri'], defaults={k: data[k] for k in keys if k in data})

        track_inst, created = get_or_create(Track, track_data)
        if force_update or created:
            if 'artists' in track_data:
                for artist_data in track_data['artists']:
                    artist_inst, _ = get_or_create(Artist, artist_data)
                    track_inst.artists.add(artist_inst)
            if 'album' in track_data:
                album_data = track_data['album']
                album_inst, created = get_or_create(Album, album_data)
                if created:
                    if 'artists' in album_data:
                        for artist_data in album_data['artists']:
                            artist_inst, _ = get_or_create(Artist, artist_data)
                            album_inst.artists.add(artist_inst)
                        album_inst.get_cover()
                        album_inst.save()
                track_inst.album = album_inst
            track_inst.length = track_data['length']
            track_inst.save()
            track_inst.get_lyrics()
        return track_inst

    @classmethod
    def current_from_mopidy(cls):
        return cls.get_or_create_from_mopidy(mopidy_api('core.playback.get_current_tl_track')['track'])

    @classmethod
    def add_random(cls):
        if mopidy_api('core.tracklist.get_length') < 10:
            old_enough = models.Q(last_play=None) | models.Q(last_play__lt=timezone.now() - timedelta(hours=1))
            active = models.Q(playlisttrack__playlist__active=True)
            current = models.Q(uri__in=set(t['uri'] for t in mopidy_api('core.tracklist.get_tracks')))
            track = cls.objects.filter(old_enough, active).exclude(current).order_by('?').first()
            if track:
                print(f'Randomly added {track}')
                mopidy_api('core.tracklist.add', uri=track.uri)
            else:
                track = cls.objects.filter(active).exclude(current).order_by('?').first()
                if track:
                    print(f'Randomly added already played recently {track}')
                    mopidy_api('core.tracklist.add', uri=track.uri)
                else:
                    print("can't add a random track from an active playlist not already in the current tracklist")


class Playlist(NamedModel):
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def json(self):
        return {'name': self.name, 'uri': self.uri, 'active': self.active}

    def update_from_mopidy(self):
        self.playlisttrack_set.all().delete()
        for i, track in enumerate(mopidy_api('core.playlists.get_items', uri=self.uri)):
            track_inst, created = Track.objects.get_or_create(uri=track['uri'], defaults={'name': track['name']})
            if created:
                track_inst.update_from_mopidy()
            PlaylistTrack(playlist=self, number=i, track=track_inst).save()

    @classmethod
    def create_from_mopidy(cls):
        for playlist in mopidy_api('core.playlists.as_list'):
            defaults = {'name': playlist['name'], 'active': True}
            playlist_inst, created = Playlist.objects.get_or_create(uri=playlist['uri'], defaults=defaults)
            print(f'Updating playlist {playlist_inst}')
            playlist_inst.update_from_mopidy()


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist)
    number = models.IntegerField()
    track = models.ForeignKey(Track)

    def __str__(self):
        return f'{self.playlist} - {self.number} - {self.track}'

    class Meta:
        unique_together = ('playlist', 'number')
        ordering = ('playlist', 'number')

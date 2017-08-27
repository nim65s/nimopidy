from json import dumps
from random import choice

from channels import Channel, Group

from .models import Album, Artist, Playlist, Track
from .utils import mopidy_api, telnet_snapcast


def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group('clients').add(message.reply_channel)
    Channel('snapcast').send({})


def ws_disconnect(message):
    Group('clients').discard(message.reply_channel)


def mopidy(message):
    def process_track(track_data):
        def get_or_create(model, data):
            keys = ['name', 'uri', 'date', 'length', 'disc_no', 'track_no']
            return model.objects.get_or_create(**{key: data[key] for key in keys if key in data})

        track_inst, created = get_or_create(Track, track_data)
        if created:
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
            track_inst.save()
            track_inst.get_lyrics()
        return track_inst

    if 'status_report' in message.content:
        if message.content['status_report']['current_track']:
            track_inst = process_track(message.content['status_report']['current_track'])
            Group('clients').send({'text': dumps({
                'track': track_inst.json(),
                'time_position': message.content['status_report']['time_position'],
                'state': message.content['status_report']['state'],
            })})
        else:
            tracklist('plop')
            mopidy_api('core.playback.play')
            mopidy_api('core.tracklist.set_consume', value=True)
    elif 'playback_state_changed' in message.content:
        Group('clients').send({'text': dumps({
            'state': message.content['playback_state_changed']['new_state'],
        })})
    elif 'track_playback_started' in message.content:
        track_inst = process_track(message.content['track_playback_started']['tl_track']['track'])
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': 0,
        })})
    elif 'track_playback_ended' in message.content:
        track_inst = process_track(message.content['track_playback_ended']['tl_track']['track'])
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': message.content['track_playback_ended']['time_position'],
        })})
        Channel('tracklist').send({})
    elif 'track_playback_paused' in message.content:
        track_inst = process_track(message.content['track_playback_paused']['tl_track']['track'])
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': message.content['track_playback_paused']['time_position'],
        })})
    elif 'track_playback_resumed' in message.content:
        track_inst = process_track(message.content['track_playback_resumed']['tl_track']['track'])
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': message.content['track_playback_resumed']['time_position'],
        })})
    elif 'seeked' in message.content:
        Group('clients').send({'text': dumps({
            'time_position': message.content['seeked']['time_position'],
        })})
    elif 'tracklist_changed' in message.content:
        tracklist('plop')
    elif 'options_changed' in message.content:
        pass
    else:
        print(message.content)


def snapcast(message):
    gps = telnet_snapcast("Server.GetStatus")['result']['server']['groups']
    clients = [dict(**cli['host'], **cli['config']['volume']) for gp in gps for cli in gp['clients']]
    Group('clients').send({'text': dumps({
        'snapclients': clients,
    })})


def tracklist(message):
    if mopidy_api('core.tracklist.get_length') < 10:
        playlist = Playlist.objects.filter(active=True).order_by('?').first()
        tracks = mopidy_api('core.playlists.get_items', uri=playlist.uri)
        mopidy_api('core.tracklist.add', uri=choice(tracks)['uri'])

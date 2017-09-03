from json import dumps

from django.utils import timezone

from channels import Channel, Group

from .models import Track
from .utils import start, telnet_snapcast


def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group('clients').add(message.reply_channel)
    Channel('snapcast').send({})


def ws_disconnect(message):
    Group('clients').discard(message.reply_channel)


def mopidy(message):
    if 'status_report' in message.content:
        if message.content['status_report']['current_track']:
            track_inst = Track.get_or_create_from_mopidy(message.content['status_report']['current_track'])
            Group('clients').send({'text': dumps({
                'track': track_inst.json(),
                'time_position': message.content['status_report']['time_position'],
                'state': message.content['status_report']['state'],
            })})
        else:
            start()
            Track.add_random()
    elif 'playback_state_changed' in message.content:
        Group('clients').send({'text': dumps({
            'state': message.content['playback_state_changed']['new_state'],
        })})
    elif 'track_playback_started' in message.content:
        track_inst = Track.get_or_create_from_mopidy(message.content['track_playback_started']['tl_track']['track'])
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': 0,
        })})
    elif 'track_playback_ended' in message.content:
        track_inst = Track.get_or_create_from_mopidy(message.content['track_playback_ended']['tl_track']['track'])
        track_inst.playcount += 1
        track_inst.last_play = timezone.now()

        track_inst.save()
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': message.content['track_playback_ended']['time_position'],
        })})
        Track.add_random()
    elif 'track_playback_paused' in message.content:
        track_inst = Track.get_or_create_from_mopidy(message.content['track_playback_paused']['tl_track']['track'])
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': message.content['track_playback_paused']['time_position'],
        })})
    elif 'track_playback_resumed' in message.content:
        track_inst = Track.get_or_create_from_mopidy(message.content['track_playback_resumed']['tl_track']['track'])
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': message.content['track_playback_resumed']['time_position'],
        })})
    elif 'seeked' in message.content:
        Group('clients').send({'text': dumps({
            'time_position': message.content['seeked']['time_position'],
        })})
    elif 'tracklist_changed' in message.content:
        Track.add_random()
    elif 'options_changed' in message.content:
        pass
    elif 'playlists_loaded' in message.content:
        start()
        Track.add_random()
    else:
        print(f'message de mopidy inconnu: {message.content}')


def snapcast(message):
    gps = telnet_snapcast("Server.GetStatus")['result']['server']['groups']
    clients = [dict(**cli['host'], **cli['config']['volume']) for gp in gps for cli in gp['clients']]
    Group('clients').send({'text': dumps({
        'snapclients': clients,
    })})

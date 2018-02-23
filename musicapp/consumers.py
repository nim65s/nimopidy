from json import loads

from django.http import JsonResponse
from django.utils import timezone

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import add_random, get_or_create_from_mopidy
from .utils import start, telnet_snapcast


class WSConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self, event):
        await self.accept()
        await self.channel_layer.group_add('clients', self.channel_name)
        await self.channel_layer.group_send('music', {'type': 'snapcast'})

    async def disconnect(self, event):
        await self.channel_layer.group_discard('clients', self.channel_name)


class MusicConsumer(AsyncConsumer):
    @database_sync_to_async
    def playcount(self, track):
        track.playcount += 1
        track.last_play = timezone.now()
        track.save()

    async def mopidy(self, message):
        if 'status_report' in message.content:
            if message.content['status_report']['current_track']:
                track_inst = await get_or_create_from_mopidy(message.content['status_report']['current_track'])
                await self.channel_layer.group_send('clients', {
                    'track': track_inst.json(),
                    'time_position': message.content['status_report']['time_position'],
                    'state': message.content['status_report']['state'],
                })
            else:
                await start()
                await add_random()
        elif 'playback_state_changed' in message.content:
            await self.channel_layer.group_send('clients', {
                'state': message.content['playback_state_changed']['new_state'],
            })
        elif 'track_playback_started' in message.content:
            track_inst = await get_or_create_from_mopidy(message.content['track_playback_started']['tl_track']['track'])
            await self.channel_layer.group_send('clients', {
                'track': track_inst.json(),
                'time_position': 0,
            })
        elif 'track_playback_ended' in message.content:
            track_inst = await get_or_create_from_mopidy(message.content['track_playback_ended']['tl_track']['track'])
            await self.playcount(track_inst)
            await self.channel_layer.group_send('clients', {
                'track': track_inst.json(),
                'time_position': message.content['track_playback_ended']['time_position'],
            })
            await add_random()
        elif 'track_playback_paused' in message.content:
            track_inst = await get_or_create_from_mopidy(message.content['track_playback_paused']['tl_track']['track'])
            await self.channel_layer.group_send('clients', {
                'track': track_inst.json(),
                'time_position': message.content['track_playback_paused']['time_position'],
            })
        elif 'track_playback_resumed' in message.content:
            track_inst = await get_or_create_from_mopidy(message.content['track_playback_resumed']['tl_track']['track'])
            await self.channel_layer.group_send('clients', {
                'track': track_inst.json(),
                'time_position': message.content['track_playback_resumed']['time_position'],
            })
        elif 'seeked' in message.content:
            await self.channel_layer.group_send('clients', {
                'time_position': message.content['seeked']['time_position'],
            })
        elif 'tracklist_changed' in message.content:
            await add_random()
        elif 'options_changed' in message.content:
            pass
        elif 'playlists_loaded' in message.content:
            await start()
            await add_random()
        else:
            print(f'message de mopidy inconnu: {message.content}')

    async def snapcast(self, message):
        gps = await telnet_snapcast("Server.GetStatus")['result']['server']['groups']
        clients = [dict(**cli['host'], **cli['config']['volume']) for gp in gps for cli in gp['clients']]
        await self.channel_layer.group_send('clients', {
            'snapclients': clients,
        })


# TODO: remettre ça dans les vues
class WebhookConsumer(AsyncConsumer):
    async def http_request(self, body):
        msg = loads(body)
        msg['type'] = 'nimopidy'
        await self.channel_layer.send('music', msg)


class SnapcastConsumer(AsyncConsumer):
    async def http_request(self, body):
        await telnet_snapcast("Client.SetVolume", loads(body))
        await self.channel_layer.send('music', {'type': 'snapcast'})

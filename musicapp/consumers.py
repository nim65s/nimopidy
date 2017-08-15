from json import dumps

from channels import Group

from .models import Album, Artist, Track


def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group('clients').add(message.reply_channel)


def ws_disconnect(message):
    Group('clients').discard(message.reply_channel)


def mopidy(message):
    if 'status_report' in message.content:
        def get_or_create(model, data):
            keys = ['name', 'uri', 'date', 'length']
            return model.objects.get_or_create(**{key: data[key] for key in keys if key in data})

        if 'current_track' in message.content['status_report']:
            track_data = message.content['status_report']['current_track']
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
                            album_inst.save()
                    track_inst.album = album_inst
                track_inst.save()
                track_inst.get_lyrics()
        Group('clients').send({'text': dumps({
            'track': track_inst.json(),
            'time_position': message.content['status_report']['time_position'],
            'state': message.content['status_report']['state'],
        })})
    else:
        print(message.content)

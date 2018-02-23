from json import loads
from time import sleep

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .models import ACTIONS, Event, Playlist, Track
from .utils import mopidy_api, start


@csrf_exempt
def playlists(request):
    if request.method == 'POST':
        req = loads(request.body)
        Playlist.objects.filter(uri=req['uri']).update(active=req['active'])
    return JsonResponse({'playlists': [pl.json() for pl in Playlist.objects.all()]})


def start_view(request):
    while True:
        try:
            Track.add_random()
            start()
            break
        except Exception as e:
            print(f'fail: {e}')
            print('starting in 5…')
            sleep(5)
    print('started')
    return JsonResponse({})


class TrackUpdateView(UpdateView):
    model = Track
    fields = ['lyrics']
    slug_field = 'uri'
    success_url = '/'


@login_required
def remove_track(request, tlid):
    data = mopidy_api('core.tracklist.remove', criteria={'tlid': [tlid]})[0]
    track = Track.get_or_create_from_mopidy(track_data=data['track'])
    Event.objects.create(user=request.user, action=ACTIONS.remove, track=track)
    return JsonResponse({'result': 'ok'})


@login_required
def next(request):
    data = mopidy_api('core.playback.get_current_track')
    track = Track.get_or_create_from_mopidy(track_data=data)
    Event.objects.create(user=request.user, action=ACTIONS.next, track=track)
    mopidy_api('core.playback.next')
    return JsonResponse({'result': 'ok'})

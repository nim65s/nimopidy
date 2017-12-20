from json import loads
from time import sleep

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from channels import Channel

from .models import Playlist, Track
from .utils import start, telnet_snapcast


@csrf_exempt
def webhooks(request):
    Channel('mopidy').send(loads(request.body))
    return JsonResponse({})


@csrf_exempt
def snapcast(request):
    telnet_snapcast("Client.SetVolume", loads(request.body))
    Channel('snapcast').send({})
    return JsonResponse({})


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

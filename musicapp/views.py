from json import loads

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from channels import Channel

from .models import Playlist
from .utils import telnet_snapcast


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

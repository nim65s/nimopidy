from json import loads

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from channels import Channel

from .utils import telnet_snapcast


@csrf_exempt
def webhooks(request):
    Channel('mopidy').send(loads(request.body))
    return JsonResponse({})


def snapcast(request, target, muted, percent):
    telnet_snapcast("Client.SetVolume", {'id': target, 'volume': {'muted': bool(int(muted)), 'percent': int(percent)}})
    Channel('snapcast').send({})
    return JsonResponse({})

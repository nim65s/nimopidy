from json import loads

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from channels import Channel


@csrf_exempt
def webhooks(request):
    Channel('mopidy').send(loads(request.body))
    return JsonResponse({})

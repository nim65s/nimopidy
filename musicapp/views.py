from json import loads

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from channels import Channel
from rest_framework import viewsets

from .models import Track
from .serializers import TrackSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_fields = ('uri', 'artist', 'title')


@csrf_exempt
def webhooks(request):
    Channel('mopidy').send(loads(request.body))
    return JsonResponse({})

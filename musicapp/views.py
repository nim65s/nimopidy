from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets

from .models import Song
from .serializers import SongSerializer


@csrf_exempt
def lyrics(request, uri):
    song, created = Song.objects.get_or_create(uri=uri)
    if created:
        song.artist = request.POST.get('artist')
        song.title = request.POST.get('title')
        song.get_lyrics()
    return JsonResponse(song.json())


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_fields = ('uri', 'artist', 'title')

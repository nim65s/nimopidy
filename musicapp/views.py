from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

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


def update_lyrics(request, uri):
    song = get_object_or_404(Song, uri=uri)
    song.get_lyrics()
    return redirect('/')


class SongUpdateView(UpdateView):
    model = Song
    fields = ['lyrics']
    slug_field = 'uri'
    slug_url_kwarg = 'uri'


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_fields = ('uri', 'artist', 'title')

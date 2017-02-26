from rest_framework import serializers

from .models import Song


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('uri', 'lyrics', 'artist', 'title')

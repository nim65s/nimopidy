from rest_framework import serializers

from .models import Track


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('uri', 'lyrics', 'artist', 'title')

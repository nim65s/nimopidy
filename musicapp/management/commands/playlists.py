from django.core.management.base import BaseCommand

from musicapp.models import Playlist


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Playlist.update()

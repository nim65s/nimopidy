from time import sleep

from django.core.management.base import BaseCommand

from musicapp.models import Playlist


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            try:
                Playlist.create_from_mopidy()
                break
            except Exception:
                sleep(5)

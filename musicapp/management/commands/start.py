from time import sleep

from django.core.management.base import BaseCommand

from musicapp.models import Track
from musicapp.utils import start


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            try:
                Track.add_random()
                start()
                break
            except:
                sleep(5)

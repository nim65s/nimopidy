from time import sleep

from django.core.management.base import BaseCommand

from asgiref.sync import async_to_sync
from musicapp.models import add_random
from musicapp.utils import start


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            try:
                async_to_sync(add_random)()
                async_to_sync(start)()
                break
            except Exception:
                sleep(5)

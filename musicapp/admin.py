from django.contrib.admin import site

from .models import Song

site.register(Song)

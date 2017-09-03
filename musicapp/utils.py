from datetime import timedelta
from json import dumps, loads
from random import choice
from telnetlib import Telnet

from django.conf import settings
from django.utils import timezone

import html2text
import requests
from bs4 import BeautifulSoup

WIKIA = 'http://lyrics.wikia.com/'


def soup_to_lyrics(soup):
    if not isinstance(soup, BeautifulSoup):
        soup = BeautifulSoup(soup, 'html.parser')
    return soup.find_all('div', class_='lyricbox')


def get_lyrics(artist, song):
    req = requests.get("%s%s:%s" % (WIKIA, artist, song.split('-')[0].title()))
    soup = BeautifulSoup(req.content, 'html.parser')
    lyrics = soup_to_lyrics(soup)
    if not lyrics:
        search = soup.find_all('a', class_='external text')
        if search:
            req_s = requests.get(search[0].attrs['href'])
            search_page = BeautifulSoup(req_s.content, 'html.parser').find_all('a', class_='result-link')
            if search_page:
                req_final = requests.get(search_page[0].attrs['href'])
                lyrics = soup_to_lyrics(req_final.content)
        elif 'disambiguation' in str(req.content):
            disambiguation = requests.get(WIKIA + soup.find('div', id='mw-content-text').find('a').attrs['href'])
            lyrics = soup_to_lyrics(disambiguation.content)
    return html2text.html2text(str(lyrics)[1:-1]) if lyrics else req.url


def telnet_snapcast(method, params=None):
    with Telnet(settings.SNAPSERVER_HOST, settings.SNAPSERVER_PORT) as tn:
        data = {"id": 1, "jsonrpc": "2.0", "method": method}
        if params is not None:
            data["params"] = params
        tn.write(dumps(data).encode() + b'\r\n')
        return loads(tn.read_until(b'\r\n').decode())


def mopidy_api(method, **kwargs):
    data = {"jsonrpc": "2.0", "id": 1, "method": method}
    if kwargs:
        data['params'] = kwargs
    r = requests.post(f"http://{settings.MOPIDY_HOST}:{settings.MOPIDY_PORT}/mopidy/rpc", data=dumps(data))
    r.raise_for_status()
    return r.json()['result']


def add_random():
    from .models import Track, Playlist  # noqa

    if mopidy_api('core.tracklist.get_length') < 10:
        for _ in range(10):
            playlist = Playlist.objects.filter(active=True).order_by('?').first()
            if not playlist:
                break
            track = choice(mopidy_api('core.playlists.get_items', uri=playlist.uri))
            track_inst = Track.get_or_create_from_mopidy(uri=track['uri'])
            if not track_inst.last_play or timezone.now() - track_inst.last_play > timedelta(hours=1):
                print(f'Randomly added {track["name"]} from {playlist}')
                mopidy_api('core.tracklist.add', uri=track['uri'])
                break
        else:
            print("Can't find a random track to add")

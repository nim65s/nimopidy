import asyncio
from json import dumps, loads

from django.conf import settings

import html2text
from bs4 import BeautifulSoup
from requests_threads import AsyncSession

WIKIA = 'http://lyrics.wikia.com/'

session = AsyncSession()


def soup_to_lyrics(soup):
    if not isinstance(soup, BeautifulSoup):
        soup = BeautifulSoup(soup, 'html.parser')
    return soup.find_all('div', class_='lyricbox')


async def get_lyrics(artist, song):
    req = await session.get("%s%s:%s" % (WIKIA, artist, song.split('-')[0].title()))
    soup = BeautifulSoup(req.content, 'html.parser')
    lyrics = soup_to_lyrics(soup)
    if not lyrics:
        search = soup.find_all('a', class_='external text')
        if search:
            req_s = await session.get(search[0].attrs['href'])
            search_page = BeautifulSoup(req_s.content, 'html.parser').find_all('a', class_='result-link')
            if search_page:
                req_final = await session.get(search_page[0].attrs['href'])
                lyrics = soup_to_lyrics(req_final.content)
        elif 'disambiguation' in str(req.content):
            disambiguation = await session.get(WIKIA + soup.find('div', id='mw-content-text').find('a').attrs['href'])
            lyrics = soup_to_lyrics(disambiguation.content)
    return html2text.html2text(str(lyrics)[1:-1]) if lyrics else req.url


async def telnet_snapcast(method, params=None):
    # TODO with statement
    reader, writer = yield asyncio.open_connection(settings.SNAPSERVER_HOST, settings.SNAPSERVER_PORT)
    data = {"id": 1, "jsonrpc": "2.0", "method": method}
    if params is not None:
        data["params"] = params
    writer.write(dumps(data).encode() + b'\r\n')
    yield loads(reader.readuntil(b'\r\n').decode())
    writer.close()


async def mopidy_api(method, **kwargs):
    data = {"jsonrpc": "2.0", "id": 1, "method": method}
    if kwargs:
        data['params'] = kwargs
    r = await session.post(f"http://{settings.MOPIDY_HOST}:{settings.MOPIDY_PORT}/mopidy/rpc", data=dumps(data))
    try:
        return r.json()['result']
    except Exception:
        return []


async def start():
    if not mopidy_api('core.tracklist.get_consume'):
        await mopidy_api('core.tracklist.set_consume', value=True)
        print('set consume')
    if mopidy_api('core.playback.get_state') == 'stopped':
        await mopidy_api('core.playback.play')
        print('play')

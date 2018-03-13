# NiMoPiDy

A collaborative music player that can play simultaneously in multiple rooms and from many sources (for now, only local,
youtube, and spotify have been tested)

Anybody can add a song from any source in the tracklist, and random songs from selected playlists that
have not been played in the last hour are added when there is less than 10 songs in the tracklist.

Can be controlled from the web app or from any mpd client.

Shows lyrics and album covers.

Uses [mopidy](https://docs.mopidy.com/en/latest/), [snapcast](https://github.com/badaix/snapcast) and/or
[icecast](http://icecast.org/), [django](https://www.djangoproject.com/),
[channels](https://channels.readthedocs.io/en/stable/), and [react](https://facebook.github.io/react/).

## Chat about this project

[#nimopidy:matrix.org](https://riot.im/app/#/room/#nimopidy:matrix.org)

## Launch everything with docker-compose

### Exemple Configuration

```
echo NIMOPIDY_HOST=$(hostname -f) >> .env
echo POSTGRES_PASSWORD=$(openssl rand -base64 32) >> .env
echo SECRET_KEY=$(openssl rand -base64 32) >> .env
```

- `conf/mopidy_local/mopidy.conf`:
```
[spotify]
username = Nim65s
password = Euyohh8ousah6AiRAing1pah
client_id = 1ee8c67a-b625-411a-959d-a326becc0a12
client_secret = JaT_eeh8Ain8pyi9D_iB0gee6ueifeiWs_W_NvS_Cok=
bitrate = 160
```

Get a premium account and your own passwords, those ones are fake :)
You can get `client_id` & `client_secret` on [mopidy's website](https://www.mopidy.com/authenticate/#spotify).


### Reverse Proxy

This project needs a running [traefik](https://traefik.io) instance. If you don't have one, look at those examples for
[dev](https://github.com/nim65s/traefik-dev) and [prod](https://github.com/nim65s/traefik-prod).

### Start

```
docker-compose up -d
docker-compose exec daphne ./manage.py playlists
```

### Shell

```
docker-compose exec daphne pip install ipython
docker-compose exec daphne ./manage.py shell
```

Go to `http://nimopidy.local` (check your DNS settings, or your /etc/hosts), and/or launch `snapserver -h nimopidy` from your clients

## TODO

- playlist management
    - add a song to a playlist
    - diff two playlists
    - remove duplicates
- shuffle tracklist
- lyrics versionning (django-reversion)
- search in selected/all playlists
- translations
- https://github.com/jwilder/dockerize
    - use alpine instead of arch
    - wait for stuff
    - generate unique mopidy configuration file

## Later

- Build android app http://jkaufman.io/react-web-native-codesharing/
- Timing / kara / performous
- votes
- whitelist / blacklist / modération
- find similar songs
    - same artist / name
    - covers
    - live

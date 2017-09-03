# NiMoPiDy

## Chat about this project

[#nimopidy:matrix.org](https://riot.im/app/#/room/#nimopidy:matrix.org)

## Launch everything with docker-compose

`docker-compose up`

(First launch can be *really* long)

## Install

You need: 

- a DNS where 'nimopidy' points to your server
- [snapcast](https://github.com/badaix/snapcast)
- [redis](https://redis.io/)
- [postgres](https://www.postgresql.org/)
- [mopidy](https://docs.mopidy.com/en/latest/)
- a [virtualenv](https://virtualenv.pypa.io/en/stable/) (recommended)

- configure mopidy for snapcast & nimopidy's backend

```
[audio]
output = audioresample ! audioconvert ! audio/x-raw,rate=48000,channels=2,format=S16LE ! wavenc ! filesink location=/tmp/snapfifo

[webhooks]
webhook_url = http://nimopidy/webhooks
api_key = whocares
```

- create a user for postgres:

```sql
create user nimopidy with password '<POSTGRES_PASSWORD>';
create database nimopidy owner nimopidy;
```

- setup the [django](https://www.djangoproject.com/) backend:

```bash
mkdir /etc/nimopidy
echo '<POSTGRES_PASSWORD>' > /etc/nimopidy/db_password
openssl rand -base64 32 > /etc/nimopidy/secret_key
pip install -U -r requirements.txt
./manage.py migrate
./manage.py playlists # populates database from mopidy, can be really long, but you don't have to wait for it to finish
./manage.py createsuperuser # optional, if you want to access to the admin interface
./manage.py runserver
```

- setup the [react](https://facebook.github.io/react/) frontend:

```bash
npm install
npm run build
./manage.py collectstatic
```

- setup  [nginx](https://nginx.org/en/)

```
server {
    server_name  nimopidy;
    listen       80;

    access_log  logs/nimopidy.access.log;
    error_log  logs/nimopidy.access.err;

    tcp_nodelay on;

    location /static {
        alias /srv/nimopidy/static;
        expires 30d;
    }

    location /media {
        alias /srv/nimopidy/media;
        expires 30d;
    }

    location / {
        proxy_pass http://nimopidy:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
    }
}


```

## TODO

- update / modify: lyrics, cover & infos
- playlist management
    - add a song to a playlist
    - diff two playlists
    - remove duplicates
- shuffle tracklist
- lyrics versionning (django-reversion)
- search in selected playlists

## Later

- Build android app http://jkaufman.io/react-web-native-codesharing/
- django-knocker (desktop notifications)
- Timing / kara / performous
- votes
- whitelist / blacklist / modération
- find similar songs
    - same artist / name
    - covers
    - live


## Find stuff in Mopidy API

### describe

curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}' http://localhost:6680/mopidy/rpc|jq
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}' http://localhost:6680/mopidy/rpc|jq . | grep '^    "'|sort
echo -e (curl -s -d '{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}' http://localhost:6680/mopidy/rpc|jq '.result."core.tracklist.filter".description')

### get playlists

curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.playlists.get_playlists", "params": {"include_tracks": false}}' http://localhost:6680/mopidy/rpc|jq
curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.playlists.as_list"}' http://localhost:6680/mopidy/rpc|jq

### get images

curl -d '{"jsonrpc": "2.0", "id": 1, "method": "core.library.get_images", "params": {"uris": ["spotify:track:4xEIrUbZn1ySRuFbVv6dl9"]}}' http://localhost:6680/mopidy/rpc|jq

### tracklist

$r.mopidy.tracklist.getTlTracks().done(data => console.log(data));

### Search

curl -s -d '{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}' http://localhost:6680/mopidy/rpc|jq '.result."core.library.search"'
echo -e (curl -s -d '{"jsonrpc": "2.0", "id": 1, "method": "core.describe"}' http://localhost:6680/mopidy/rpc|jq '.result."core.library.search".description')

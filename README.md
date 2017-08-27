# NiMoPiDy

## Install

setup virtualenv and redis, then:

```bash
pip install -U -r requirements.txt
npm install
npm run build
./manage.py migrate
./manage.py runserver
```

## TODO

- django-knocker (desktop notifications)
- playlist management
- responsive
- update / modify: lyrics, cover & infos
- shuffle tracklist


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

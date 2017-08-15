from channels.routing import route

from musicapp.consumers import mopidy, ws_connect, ws_disconnect

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
    route('mopidy', mopidy),
]

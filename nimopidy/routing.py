from channels.routing import route

from musicapp.consumers import mopidy, snapcast, ws_connect, ws_disconnect, ws_receive

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
    route('websocket.receive', ws_receive),
    route('mopidy', mopidy),
    route('snapcast', snapcast),
]

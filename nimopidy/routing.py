from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ChannelNameRouter, ProtocolTypeRouter
from musicapp.consumers import MusicConsumer, WSConsumer

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        'music': MusicConsumer
    }),
    'http': AuthMiddlewareStack(AsgiHandler),
    'websocket': AuthMiddlewareStack(WSConsumer),
})

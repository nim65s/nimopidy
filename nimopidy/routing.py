from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from musicapp.consumers import MusicConsumer, SnapcastConsumer, WebhooksConsumer, WSConsumer

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        'music': MusicConsumer
    }),
    'http': AuthMiddlewareStack(URLRouter([
        path('webhooks', WebhooksConsumer, name='webhooks'),
        path('snapcast', SnapcastConsumer, name='snapcast'),
        path('', AsgiHandler),
    ])),
    'websocket': AuthMiddlewareStack(WSConsumer),
})

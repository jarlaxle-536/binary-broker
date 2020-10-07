from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.auth import AuthMiddlewareStack
import json

import binary_broker.applications.trading.channel_routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        binary_broker.applications.trading.channel_routing.urlpatterns
    )
})

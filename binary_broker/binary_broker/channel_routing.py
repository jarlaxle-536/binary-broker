from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.auth import AuthMiddlewareStack
import json

import binary_broker.applications.trading.channel_routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            binary_broker.applications.trading.channel_routing.urlpatterns
        )
    ),
})

channel_layer = get_channel_layer()
print(channel_layer)
text = 'hello'
group_name = 'trading_broadcast'
async_to_sync(channel_layer.group_send)(
    group_name,
    {"type": "celery.message",
     "text": json.dumps(text)
     })

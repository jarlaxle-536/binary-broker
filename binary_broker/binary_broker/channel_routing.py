from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import binary_broker.applications.trading.channel_routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            binary_broker.applications.trading.channel_routing.urlpatterns
        )
    ),
})

#application = [
#    route('websocket.connect', ws_connect),
#    route('websocket.disconnect', ws_disconnect),
#]

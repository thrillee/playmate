from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chats.consumers import ChatConsumer
from chats.auth import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter([
                url(r"^(?P<pk>[0-9]+)/(?P<id>[0-9]+)/message/$", ChatConsumer),
            ])
        )
    )
})

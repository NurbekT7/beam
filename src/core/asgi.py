import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from core.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        URLRouter(websocket_urlpatterns)
    ),
})

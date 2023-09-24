import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from frontend.routing import websocket_urlpatterns
from frontend.consumers import SensorDataConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic_dashboard.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        URLRouter([path('ws', SensorDataConsumer.as_asgi())])
})

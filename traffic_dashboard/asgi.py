import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import backend.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_dashboard.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(backend.routing.websocket_urlpatterns)
    )
})

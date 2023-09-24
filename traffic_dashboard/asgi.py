# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from backend.consumers import SensorDataConsumer
# import traffic_dashboard

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic_dashboard.settings")
# traffic_dashboard.settings.configure()

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket":
#         URLRouter([path('ws', SensorDataConsumer.as_asgi())])
# })

import os
from backend.consumers import SensorDataConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
import backend.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_dashboard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(backend.routing.websocket_urlpatterns)
        # URLRouter([path('ws', SensorDataConsumer.as_asgi())])
    )
})

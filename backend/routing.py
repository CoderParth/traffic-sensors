from django.urls import path
from .consumers import SensorDataConsumer

websocket_urlpatterns = [
    path('ws/sensor-data', SensorDataConsumer.as_asgi()),
]

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class SensorDataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Accept the WebSocket connection

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Perform cleanup if needed
#         pass

#     async def receive(self, text_data):
#         # Handle received data if needed
#         # For example, you can echo the received data back to the client
#         print("data ", text_data)
#         await self.send(text_data)


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.core import serializers
# from django.db.models import Q
# from .models import TrafficSensorData
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# import asyncio


# class SensorDataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send_sensor_data_periodically()

#     async def disconnect(self, close_code):
#         print("Websocket Disconnected")
#         pass

#     async def receive(self, text_data):
#         print("data ", text_data)
#         await self.send(text_data)

#     async def send_sensor_data_periodically(self):
#         loop = asyncio.get_event_loop()
#         loop.create_task(self.send_sensor_data_task())

#     async def send_sensor_data_task(self):
#         while True:
#             await asyncio.sleep(5)  # Sleep for 5 seconds
#             # queryset = TrafficSensorData.objects.all()
#             # data = serializers.serialize('json', queryset)
#             await self.send(data)

# models.py in your_app_name directory

# from django.db import models
# from channels.binding.websockets import WebsocketBinding


# class IntegerValue(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     value = models.IntegerField(default=0)


# class SensorDataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send_sensor_data_periodically()

#     async def disconnect(self, close_code):
#         print("Websocket Disconnected")
#         pass

#     async def receive(self, text_data):
#         print("data ", text_data)
#         await self.send(text_data)

#     async def send_sensor_data_periodically(self):
#         loop = asyncio.get_event_loop()
#         loop.create_task(self.send_sensor_data_task())

#     async def send_sensor_data_task(self):
#         while True:
#             await asyncio.sleep(5)  # Sleep for 5 seconds
#             # queryset = TrafficSensorData.objects.all()
#             # data = serializers.serialize('json', queryset)
#             await self.send(data)


# from django.apps import apps
# import asyncio
# import json
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer

# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic_dashboard.settings")
# django.setup()
# TrafficSensorData = apps.get_model('backend', 'TrafficSensorData')


# class SensorDataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send_sensor_data_periodically()

#     async def disconnect(self, close_code):
#         print("Websocket Disconnected")
#         pass

#     async def receive(self, text_data):
#         print("data ", text_data)
#         await self.send(text_data)

#     async def send_sensor_data_periodically(self):
#         loop = asyncio.get_event_loop()
#         loop.create_task(self.send_sensor_data_task())

#     async def send_sensor_data_task(self):
#         while True:
#             await asyncio.sleep(5)  # Sleep for 5 seconds
#             data = await self.get_sensor_data()
#             await self.send(json.dumps(data))

#     @database_sync_to_async
#     def get_sensor_data(self):
#         # return "This will be sent"
#         print("Okay connected boy")
#         queryset = TrafficSensorData.objects.all()
#         # Modify the following line if your model has different field names
#         return [{"timestamp": str(obj.timestamp), "latitude": obj.latitude, "longitude": obj.longitude, "vehicle_speed": obj.vehicle_speed, "speed_limit": obj.speed_limit} for obj in queryset]


import datetime
from django.apps import apps
import json
import asyncio
import os
import django
import random
from decimal import Decimal
from django.core.serializers import serialize
from django.http import HttpRequest
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_dashboard.settings')
django.setup()

TrafficSensorData = apps.get_model('backend', 'TrafficSensorData')

# fmt: off
from .views import TrafficSensorDataViewSet
from backend.serializers import TrafficSensorDataSerializer
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
# fmt: on


class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected")
        while True:
            await self.send_sensor_data_task()
            # wait for 5 seconds before sending the next update
            await asyncio.sleep(5)

    async def disconnect(self, close_code):
        print(f"WebSocket closed with code: {close_code}")

    async def receive(self, text_data):
        # Handle receiving data from WebSocket
        pass

    async def send_sensor_data_task(self):
        await self.update_sensor_data()
        data = await self.get_sensor_data()
        serialized_data = json.dumps(data)
        await self.send(text_data=serialized_data)

    @database_sync_to_async
    def get_sensor_data(self):
        # Create a basic HttpRequest object
        django_request = HttpRequest()
        # Wrap the HttpRequest object with a DRF Request object
        request = Request(django_request, parsers=[JSONParser()])
        # Create the viewset instance and pass the DRF Request object
        viewset = TrafficSensorDataViewSet(request=request)
        response = viewset.list(request)
        data = response.data

        return data

    @database_sync_to_async
    def update_sensor_data(self):
        sensor_data_objs = TrafficSensorData.objects.all()
        for sensor_data_obj in sensor_data_objs:
            # Making small random adjustments to the data
            sensor_data_obj.latitude += Decimal(random.uniform(-0.001, 0.001))
            sensor_data_obj.longitude += Decimal(random.uniform(-0.001, 0.001))
            sensor_data_obj.vehicle_speed = Decimal(random.randrange(40, 121))
            sensor_data_obj.speed_limit = Decimal(random.randrange(40, 121))
            sensor_data_obj.save()

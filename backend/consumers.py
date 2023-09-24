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


import asyncio
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import TrafficSensorData
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic_dashboard.settings")
django.setup()


class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_sensor_data_periodically()

    async def disconnect(self, close_code):
        print("Websocket Disconnected")
        pass

    async def receive(self, text_data):
        print("data ", text_data)
        await self.send(text_data)

    async def send_sensor_data_periodically(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_sensor_data_task())

    async def send_sensor_data_task(self):
        while True:
            await asyncio.sleep(5)  # Sleep for 5 seconds
            data = await self.get_sensor_data()
            await self.send(json.dumps(data))

    @database_sync_to_async
    def get_sensor_data(self):
        # return "This will be sent"
        return "Okay connected boy"
        # queryset = TrafficSensorData.objects.all()
        # # Modify the following line if your model has different field names
        # return [{"timestamp": str(obj.timestamp), "latitude": obj.latitude, "longitude": obj.longitude, "vehicle_speed": obj.vehicle_speed, "speed_limit": obj.speed_limit} for obj in queryset]

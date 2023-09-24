from django.apps import apps
import json
import asyncio
import os
import django
import random
from decimal import Decimal
from django.http import HttpRequest
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_dashboard.settings')
django.setup()

TrafficSensorData = apps.get_model('backend', 'TrafficSensorData')

# fmt: off
from .views import TrafficSensorDataViewSet
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
        # Wrap the HttpRequest object
        request = Request(django_request, parsers=[JSONParser()])
        # Create the viewset instance and pass the Request object
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

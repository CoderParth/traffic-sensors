from django.core.management.base import BaseCommand
from backend.models import TrafficSensorData
from celery import shared_task
from decimal import Decimal
import random


@shared_task
def update_sensors():
    print("Updating sensor values")
    sensors = TrafficSensorData.objects.all()
    for sensor in sensors:
        sensor.latitude += Decimal('0.05')
        sensor.vehicle_speed = random.uniform(0, 100)
        sensor.save()
        print("Successfully updated sensor data")

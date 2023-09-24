from django.core.management.base import BaseCommand
from backend.models import TrafficSensorData
from random import uniform, randrange
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed the database with  sensor data'

    def handle(self, *args, **kwargs):
        if not TrafficSensorData.objects.exists():
            for i in range(10):  # Create 10 sensor data points
                lat = uniform(-44.0, -10.0)
                lon = uniform(113.0, 154.0)
                timestamp = datetime.now() - timedelta(minutes=randrange(60))
                # random speed between 40 and 120 km/h
                vehicle_speed = randrange(40, 121)
                # random speed limit between 40 and 120 km/h
                speed_limit = randrange(40, 121)

                TrafficSensorData.objects.create(
                    latitude=lat,
                    longitude=lon,
                    timestamp=timestamp,
                    vehicle_speed=vehicle_speed,
                    speed_limit=speed_limit
                )

            self.stdout.write(self.style.SUCCESS(
                'Successfully seeded sensor data.'))
        else:
            self.stdout.write(self.style.WARNING(
                'Sensor data already exists.'))

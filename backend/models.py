from django.db import models


class TrafficSensorData(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField()
    vehicle_speed = models.DecimalField(max_digits=5, decimal_places=2)
    speed_limit = models.DecimalField(max_digits=5, decimal_places=2)

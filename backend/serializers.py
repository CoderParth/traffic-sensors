# Serializers in Django REST Framework are responsible for converting objects into data types understandable by javascript and front-end frameworks

from rest_framework import serializers
from .models import TrafficSensorData


class TrafficSensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficSensorData
        fields = '__all__'

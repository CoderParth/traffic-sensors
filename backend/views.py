from rest_framework import viewsets
from .models import TrafficSensorData
from .serializers import TrafficSensorDataSerializer
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ParseError
from datetime import datetime


class TrafficSensorDataViewSet(viewsets.ModelViewSet):
    serializer_class = TrafficSensorDataSerializer

    def get_queryset(self):
        queryset = TrafficSensorData.objects.all()

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date is not None and end_date is not None:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                queryset = queryset.filter(
                    timestamp__range=[start_date, end_date])
            except ValueError:
                raise ParseError("Invalid date format. Expected YYYY-MM-DD")

        # Filter by location
        location = self.request.query_params.get('location', None)
        if location is not None:
            try:
                lat, lon = map(float, location.split(','))
                queryset = queryset.filter(latitude=lat, longitude=lon)
            except ValueError:
                raise ParseError("Invalid location format. Expected lat,lon")

        # Filter by vehicle speed range
        min_speed = self.request.query_params.get('min_speed', None)
        max_speed = self.request.query_params.get('max_speed', None)
        if min_speed is not None and max_speed is not None:
            try:
                min_speed = float(min_speed)
                max_speed = float(max_speed)
                queryset = queryset.filter(vehicle_speed__range=[
                                           min_speed, max_speed])
            except ValueError:
                raise ParseError("Invalid speed format. Expected float")

        # Filter by speed limit
        speed_limit = self.request.query_params.get('speed_limit', None)
        if speed_limit is not None:
            try:
                speed_limit = float(speed_limit)
                queryset = queryset.filter(speed_limit=speed_limit)
            except ValueError:
                raise ParseError("Invalid speed limit format. Expected float")

        return queryset

from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TrafficSensorData
from .serializers import TrafficSensorDataSerializer
from rest_framework.exceptions import ParseError, APIException
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class TrafficSensorDataViewSet(viewsets.ModelViewSet):
    serializer_class = TrafficSensorDataSerializer
    format_kwarg = 'format'

    def handle_exception(self, exc):
        if isinstance(exc, (ParseError, ValidationError, APIException)):
            return Response(
                {'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().handle_exception(exc)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'data': response.data,
        })

    def get_queryset(self):
        queryset = TrafficSensorData.objects.all()

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date is not None and end_date is not None:
            try:
                # Convert string to datetime object
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                # Adding time to cover the whole end_date day
                end_date = datetime.strptime(
                    end_date, "%Y-%m-%d") + timedelta(days=1)

                # Making datetime objects timezone-aware
                start_date = make_aware(start_date)
                end_date = make_aware(end_date)

                # Filtering by datetime range
                queryset = queryset.filter(
                    timestamp__range=[start_date, end_date]
                )
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

        if min_speed or max_speed:  # Entering this block if either is provided
            try:
                # If values are provided, convert them to float, otherwise leave them as None
                min_speed = float(min_speed) if min_speed else None
                max_speed = float(max_speed) if max_speed else None
            except ValueError:
                raise ParseError("Invalid speed format. Expected float.")

            # Filter based on the provided values
            if min_speed and max_speed:
                if min_speed > max_speed:
                    raise ValidationError(
                        "min_speed should be less than or equal to max_speed.")
                queryset = queryset.filter(vehicle_speed__range=[
                                           min_speed, max_speed])
            elif min_speed:
                # gte stands for greater than or equal to
                queryset = queryset.filter(vehicle_speed__gte=min_speed)
            elif max_speed:
                # lte stands for less than or equal to
                queryset = queryset.filter(vehicle_speed__lte=max_speed)

        # Filter by speed limit range
        min_speed_limit = self.request.query_params.get(
            'min_speed_limit', None)
        max_speed_limit = self.request.query_params.get(
            'max_speed_limit', None)

        if min_speed_limit or max_speed_limit:  # Entering this block if either is provided
            try:
                # If values are provided, convert them to Decimal, otherwise leave them as None
                min_speed_limit = Decimal(
                    min_speed_limit) if min_speed_limit else None
                max_speed_limit = Decimal(
                    max_speed_limit) if max_speed_limit else None
            except InvalidOperation:
                raise ParseError(
                    "Invalid speed limit format. Expected decimal number.")

            # Filter based on the provided values
            if min_speed_limit and max_speed_limit:
                if min_speed_limit > max_speed_limit:
                    raise ValidationError(
                        "min_speed_limit should be less than or equal to max_speed_limit.")
                queryset = queryset.filter(
                    speed_limit__range=[min_speed_limit, max_speed_limit])
            elif min_speed_limit:
                # gte stands for greater than or equal to
                queryset = queryset.filter(speed_limit__gte=min_speed_limit)
            elif max_speed_limit:
                # lte stands for less than or equal to
                queryset = queryset.filter(speed_limit__lte=max_speed_limit)

        return queryset

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrafficSensorDataViewSet

router = DefaultRouter()
router.register('sensor-data', TrafficSensorDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

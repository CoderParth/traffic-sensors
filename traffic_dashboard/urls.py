from django.contrib import admin
from django.urls import include, path
from frontend.routing import websocket_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('backend.urls')),
    path('', include('frontend.urls')),
]

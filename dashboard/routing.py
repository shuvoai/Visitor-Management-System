from django.urls import path

from dashboard.consumers import NotificationConsumer

websocket_urlpatterns = [
    path("ws/notification/<str:room_name>", NotificationConsumer.as_asgi()),
]

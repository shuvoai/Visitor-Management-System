from django.urls import path


from analytics.consumers import AnalyticsConsumer

websocket_urlpatterns = [
    path("ws/analytics/visitor-on-site/", AnalyticsConsumer.as_asgi()),
]

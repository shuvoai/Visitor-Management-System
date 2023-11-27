"""
ASGI config for visitor_management_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os


from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from dashboard.routing import websocket_urlpatterns as dashboard_websocket_urlpatterns
from analytics.routing import websocket_urlpatterns as analytics_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'visitor_management_system.settings')

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket":
            AuthMiddlewareStack(
                URLRouter(
                    dashboard_websocket_urlpatterns + analytics_websocket_urlpatterns
                )

            )
    }
)

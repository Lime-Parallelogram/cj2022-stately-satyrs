"""
ASGI config for webapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from listener.consumers import AudioStreamConsumer, DataConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path('stream/<client_ID>', AudioStreamConsumer.as_asgi()),
        path('listen/<client_ID>', AudioStreamConsumer.as_asgi()),
        path('data', DataConsumer.as_asgi())
    ])
})

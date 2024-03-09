# routing.py
from django.urls import re_path

from .consumer import SignalConsumer

websocket_urlpatterns = [
    re_path(r'ws/call/(?P<room_id>\w+)/$', SignalConsumer.as_asgi()),
]

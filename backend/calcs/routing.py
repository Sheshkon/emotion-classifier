from django.urls import re_path
from calcs import consumers


websocket_urlpatterns = [
    re_path(r'wss/socket-server/', consumers.ChatConsumer.as_asgi())
]

from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
from django.urls import re_path
from .consumers import TextRoomConsumer
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$",TextRoomConsumer.as_asgi()),
]

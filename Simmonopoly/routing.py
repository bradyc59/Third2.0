from django.urls import re_path
from django.conf.urls import url

from Simmonopoly.consumers import MonopolyConsumer

websocket_urlpatterns = [
   url(r'^ws/join/(?P<room_code>\w+)/$', MonopolyConsumer.as_asgi()),
]

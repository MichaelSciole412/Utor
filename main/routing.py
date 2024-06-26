from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/group_chat/<int:group_id>/", consumers.GroupChatConsumer.as_asgi()),
    path("ws/direct_message/<str:dmid>/", consumers.DMConsumer.as_asgi()),
]

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from main.models import *
from django.utils.html import escape
from django.utils.dateformat import DateFormat
from django.utils import timezone
from datetime import datetime

class GroupChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = "grouproom" + str(self.group_id)
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'group_chat_join',
            'html': f'<div id="user{self.user.id}"><a class="userlink" href="/profile/{self.user.username}/">{self.user.username}</a><hr/></div>',
            'check_id': f"user{self.user.id}"
        })

        group = StudyGroup.objects.get(pk=self.group_id)
        CurrentGroupChatUser.create(self.user, group)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = self.user.username

        m = GroupChat()
        m.sender = self.user
        m.group = StudyGroup.objects.get(pk=self.group_id)
        m.message = text_data_json['message']
        m.save()

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'group_chat_message',
            'message': text_data_json['message'],
            'username': username,
            'chatobj': m
        })

    def group_chat_message(self, event):
        message = event['message']
        username = event['username']
        date_formatter = DateFormat(datetime.now())
        time_str = date_formatter.format("n/j/y g:i") + "&nbsp;" + date_formatter.format("A")
        raw_html = f"""<div class="chatbox">
                        <div class="flexrow center">
                        <div style="width: 82%;">
                          <h4 class="nomargin" style="width: 80%;"><a href="/profile/{username}" class="userlink">{username}</a></h4>
                        </div>
                        <div style="text-align: right; font-size: 11px; color: gray; margin-right: 10px; margin-top: 4px;">{time_str}</div>
                        </div>
                        <p>{escape(message)}</p>
                        <hr/>
                        </div>"""
        self.send(text_data=json.dumps({'type': 'chat', 'html': raw_html}))

    def group_chat_join(self, event):
        html = event['html']
        self.send(text_data=json.dumps({'type': 'join', 'html': html, 'check_id': event['check_id']}))

    def disconnect(self, close_code):
        CurrentGroupChatUser.objects.filter(user=self.user, group__id=self.group_id).delete()

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'group_chat_leave',
            'id_to_delete': "user" + str(self.user.id)
        })

    def group_chat_leave(self, event):
        id_to_delete = event['id_to_delete']
        self.send(text_data=json.dumps({'type': 'leave', 'id_to_delete': id_to_delete}))

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
import pytz
from datetime import datetime
class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
       
        self.room_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender_name= text_data_json['sender']

        sender=CustomUser.objects.get(username=sender_name)
        group = Group.objects.get(id=self.room_id)

        india_tz = pytz.timezone('Asia/Kolkata')
        indian_time = datetime.now(india_tz)
        timestamp = indian_time.isoformat()

        message=Message.objects.create(
            sender=sender,
            group=group,
            message_content=text,
            timestamp=timestamp
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
        {
            'type': 'chat_message',
            'message':text,
            'sender': sender_name,
            'timestamp': timestamp 
        })

        
    def chat_message(self, event):
        text = event['message']
        print("text:",text)
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': text,
            'sender': sender,
            'timestamp': timestamp
        }))
       
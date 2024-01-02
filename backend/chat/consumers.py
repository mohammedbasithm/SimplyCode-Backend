import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
# import datetime
import pytz
from datetime import datetime
class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        print('reached the consumer ------------------------------------------------------ ')

        self.room_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_id}"
        print('room_id:',self.room_id)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender_name= text_data_json['sender']

        print("group_id:",self.room_id)
        sender=CustomUser.objects.get(username=sender_name)
        group = Group.objects.get(id=self.room_id)

        # utc_now = datetime.datetime.utcnow()
        india_tz = pytz.timezone('Asia/Kolkata')
        indian_time = datetime.now(india_tz)
        # current_time = ist_now.strftime('%Y-%m-%d_%I:%M %p')
        # time_part = current_time.split('_')[1] 
        timestamp = indian_time.isoformat()

        message=Message.objects.create(
            sender=sender,
            group=group,
            message_content=text,
            timestamp=timestamp
        )
        # Serialize the message data
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
        {
            'type': 'chat_message',
            'message':text,
            'sender': sender_name,
            'timestamp': timestamp 
        })

        
    def chat_message(self, event):
        # Receive message from room group
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
       
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *

class TextRoomConsumer(WebsocketConsumer):
    async def connect(self):
        print('reached the consumer ------------------------------------------------------ ')

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        
    async def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender_id= text_data_json['sender']
        group_id = text_data_json['group_id']

        sender=CustomUser.objects.get(id=sender_id)
        group = Group.objects.get(id=group_id)

        message=Message.objects.create(
            sender=sender,
            group=group,
            message_content=text
        )
        # Serialize the message data
        message_data = {
            'text': message.message_content,
            'sender': message.sender.username,
            'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'group_id': message.group.pk  
        }

        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': text,
        #         'sender': sender
        #     }
        # )
        await self.channel_layer.group_send(
            f"chat_{group_id}",
            {
                'type': 'chat_message',
                'message': message_data
            }
        )

    async def chat_message(self, event):
        # # Receive message from room group
        # text = event['message']
        # print('text:',text)
        # sender = event['sender']
        # # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'text': text,
        #     'sender': sender
        # }))
        await self.send(text_data=json.dumps(event['message']))
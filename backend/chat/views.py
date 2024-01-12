from django.shortcuts import render
from rest_framework.views import APIView
from authentification.models import CustomUser
from .models import Group,Message
from .serializer import GroupSerializer,MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import pytz
from datetime import datetime
# Create your views here.

class FetchChatRoom(APIView):
    def get(self, request):
        user_id = request.query_params.get('id')

        user=CustomUser.objects.get(pk=user_id)
        groups=Group.objects.filter(members=user)

        serialized_groups = GroupSerializer(groups, many=True)
        
        return Response(serialized_groups.data,status=status.HTTP_200_OK)
 
class FetchMessage(APIView):
    def get(self,request):
        group_id=request.query_params.get('id')

        group = get_object_or_404(Group, pk=group_id)
        message=Message.objects.filter(group=group)
        
        serializer=MessageSerializer(message,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
class GetUsername(APIView):
    def get(self, request):
        member_ids = self.request.query_params.getlist('member_id[]')  # Retrieve multiple member IDs from query params
        usernames = []
        for member_id in member_ids:
            try:
                user = CustomUser.objects.get(id=member_id)
                usernames.append({'member_id': member_id, 'username': user.username})
            except CustomUser.DoesNotExist:
                usernames.append({'member_id': member_id, 'username': None})  # Handle non-existing users
        return Response(usernames)
    
class SaveMessage(APIView):
    def post(self,request):
        try:
            text=request.data.get('text')
            sender_name=request.data.get('sender')
            groupId=request.data.get('groupId')

            sender=CustomUser.objects.get(username=sender_name)
            group=Group.objects.get(pk=groupId)

            india_tz = pytz.timezone('Asia/Kolkata')
            indian_time = datetime.now(india_tz)
            timestamp = indian_time.isoformat()

            message=Message.objects.create(
                sender=sender,
                group=group,
                message_content=text,
                timestamp=timestamp
            )
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
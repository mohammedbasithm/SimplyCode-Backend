from django.shortcuts import render
from rest_framework.views import APIView
from authentification.models import CustomUser
from .models import Group,Message
from .serializer import GroupSerializer,MessageSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class FetchChatRoom(APIView):
    def get(self, request):
        user_id = request.query_params.get('id')
        user=CustomUser.objects.get(pk=user_id)
        groups=Group.objects.filter(members=user)
        serialized_groups = GroupSerializer(groups, many=True)
        
        return Response(serialized_groups.data,status=status.HTTP_200_OK)
from django.shortcuts import get_object_or_404 
class FetchMessage(APIView):
    def get(self,request):
        group_id=request.query_params.get('id')
        print('id:',group_id)
        group = get_object_or_404(Group, pk=group_id)
        message=Message.objects.filter(group=group)
        serializer=MessageSerializer(message,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
class GetUsername(APIView):
    def get(self, request):
        print("helloooo")
        member_ids = self.request.query_params.getlist('member_id[]')  # Retrieve multiple member IDs from query params
        usernames = []
        for member_id in member_ids:
            try:
                user = CustomUser.objects.get(id=member_id)
                usernames.append({'member_id': member_id, 'username': user.username})
            except CustomUser.DoesNotExist:
                usernames.append({'member_id': member_id, 'username': None})  # Handle non-existing users
        return Response(usernames)
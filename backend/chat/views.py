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
    
class FetchMessage(APIView):
    def get(self,request):
        group_id=request.query_params.get('id')
        group=Group.objects.get(pk=group_id)
        message=Message.objects.get(group=group)
        serializer=MessageSerializer(message,Many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

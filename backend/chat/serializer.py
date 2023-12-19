from rest_framework import serializers
from .models import Group,Message
from courses.serializers import CourseSerializer

class GroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Group
        fields = ['id', 'course', 'members', 'title', 'description']
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'group', 'message_content', 'timestamp']
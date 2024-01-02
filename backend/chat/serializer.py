from rest_framework import serializers
from .models import Group,Message
from courses.serializers import CourseSerializer

class GroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Group
        fields = ['id', 'course', 'members', 'title', 'description']
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    text = serializers.CharField(source='message_content')

    def get_sender(self, obj):
        return obj.sender.username if obj.sender else None

    def get_group(self, obj):
        return obj.group.title if obj.group else None

    class Meta:
        model = Message
        fields = ['id', 'sender', 'group', 'text', 'timestamp']

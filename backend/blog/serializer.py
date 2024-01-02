from rest_framework import serializers
from .models import BlogPost, Comments, Like
from authentification.serializers import CustomUserSerializer

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'  # You can specify the fields explicitly if needed

class CommentsSerializer(serializers.ModelSerializer):
    user=CustomUserSerializer()
    class Meta:
        model = Comments
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    author=CustomUserSerializer()
    comments = CommentsSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'

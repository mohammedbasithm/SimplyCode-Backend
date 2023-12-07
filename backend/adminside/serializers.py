from rest_framework import serializers
from authentification.models import CustomUser  # Adjust this import based on your actual app structure

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','is_active', 'username', 'email','approvel','rejected','qualification','id_proof','certificate','teacher_request','phone']

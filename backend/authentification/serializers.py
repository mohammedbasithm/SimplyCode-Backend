from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['is_superuser'] = user.is_superuser
        data['is_student'] = user.is_student
        data['is_teacher'] = user.is_teacher
        data['id']=user.id
        print('hei')
        return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username','is_active' ,'email', 'phone', 'image','is_student','date_joined','is_admin','is_teacher')
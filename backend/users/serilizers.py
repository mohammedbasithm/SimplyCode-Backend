from authentification.models import CustomUser
from rest_framework import serializers

class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','username','is_superuser','is_teacher','is_active','date_joined','email','image','phone','teacher_request']
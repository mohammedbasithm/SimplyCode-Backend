from rest_framework import serializers
from .models import Payments
from courses.serializers import CourseSerializer
from authentification.serializers import CustomUserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    course=CourseSerializer()
    user=CustomUserSerializer()
    class Meta:
        model = Payments
        fields = ('course', 'user', 'teacher', 'amount', 'status', 'is_paid', 'payment_date')
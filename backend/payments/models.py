from django.utils import timezone
from django.db import models
from courses.models import Course
from authentification.models import CustomUser
# Create your models here.

class Payments(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('success','Success'),
        ('failed','Failed'),
    ]

    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_payments')
    teacher=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='teacher_payments')
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    is_paid=models.BooleanField(default=False)
    payment_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s payment for {self.course.title}"
    
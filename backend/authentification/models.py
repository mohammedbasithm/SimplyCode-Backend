from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=12,null=True,blank=True)
    image = models.ImageField(upload_to='profile_image/',null=True,blank=True)
    is_student=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)
    address=models.CharField(max_length=512,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    approvel=models.BooleanField(default=False)
    rejected=models.BooleanField(default=False)
    qualification=models.CharField(max_length=100,null=True,blank=True)
    bank_account_number=models.CharField(max_length=14,null=True,blank=True,unique=True)
    ifsc_code = models.CharField(max_length=11,null=True,blank=True)
    id_proof=models.ImageField(upload_to='teacher_idproof/',null=True,blank=True)
    certificate=models.ImageField(upload_to='teacher_certificate/',null=True,blank=True)
    teacher_request=models.BooleanField(default=False)

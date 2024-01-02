from django.db import models
from authentification.models import CustomUser
# Create your models here.

class Category(models.Model):
    category=models.CharField(max_length=255,unique=True)
    cover_image=models.ImageField(upload_to='cat_cover_img/')

    def __str__(self):
        return self.category

class Course(models.Model):
    title=models.CharField(max_length=255)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()
    instructor=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    cover_image=models.ImageField(upload_to='course_cover_img/')
    about=models.CharField(blank=True,null=True)
    is_completed=models.BooleanField(default=False)
    is_subscripe=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    videos=models.FileField(upload_to='course_videos/')
    description=models.TextField()
    chapter=models.CharField(max_length=255)
    is_free=models.BooleanField(default=False)

    def __str__(self):
        return self.chapter
    
    
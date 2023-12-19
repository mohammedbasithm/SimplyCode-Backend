from django.db import models
from authentification.models import CustomUser
from courses.models import Course
# Create your models here.

class Group(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    members=models.ManyToManyField(CustomUser,related_name='course_group')
    title=models.CharField(max_length=255)
    description=models.TextField()

    def __str__(self):
        return self.title
    
class Message(models.Model):
    sender=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='send_messages')
    group=models.ForeignKey(Group,on_delete=models.CASCADE,null=True ,default=None)
    message_content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From:{self.sender.username} To:{self.group.title}-{self.timestamp}'
    

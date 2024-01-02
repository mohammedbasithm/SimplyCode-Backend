from django.db import models
from authentification.models import CustomUser
# Create your models here.

class BlogPost(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='blog_images/',null=True,blank=True)
    

    def __str__(self):
        return self.title

class Comments(models.Model):
    blog_post=models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    blog_post=models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
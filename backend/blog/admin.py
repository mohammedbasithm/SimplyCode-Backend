from django.contrib import admin
from .models import BlogPost,Comments,Like
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Comments)
admin.site.register(Like)
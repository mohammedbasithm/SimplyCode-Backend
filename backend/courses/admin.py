from django.contrib import admin
from .models import Category,Course,Chapter

# Register your models here.
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Chapter)
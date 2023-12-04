from rest_framework import serializers
from .models import Category ,Course,Chapter

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'category','cover_image'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields='id','title','category','description','instructor','price','cover_image','about'

class ChapterSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Chapter
        fields='id','course','videos','description','chapter'
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category,Course,Chapter
from rest_framework.response import Response
from .serializers import CategorySerializer,CourseSerializer,ChapterSerilizer
from authentification.models import CustomUser
from rest_framework import status

# Create your views here.
class AddCourse(APIView):
    def post(self,request):
        try:
            courseName=request.data.get('coursename')
            price=request.data.get('price')

            category_name=request.data.get('category')
            category=Category.objects.get(category=category_name)
            
            description=request.data.get('description')
            about=request.data.get('about')
            coverimage=request.data.get('coverimage')
            print('/////////////')
            user_id=request.data.get('user_id')
            teacher=CustomUser.objects.get(pk=user_id)
            print('/////////////')
            Course.objects.create(
                title=courseName,
                category=category,
                description=description,
                instructor=teacher,
                price=price,
                cover_image=coverimage,
                about=about

            )
            print('/////////////')
            return Response({'message':'Course submission Successfuly..'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'Submission Faild..'},status=status.HTTP_400_BAD_REQUEST)
class FetchCategory(APIView):
    def get(self,request):
        category=Category.objects.all()
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data)

class ListCourse(AddCourse):
    def get(self,request):
        try:
            user_id=request.query_params.get('user_id')
            print(user_id)
            user=CustomUser.objects.get(pk=user_id)
            print(user)
            course=Course.objects.filter(instructor=user,is_completed=False)
            print(course)
            serializer=CourseSerializer(course,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class CourseDetails(APIView):
    def get(self,request):
        try:
            course_id=request.query_params.get('id')
            print('user_id:',course_id)
            course=Course.objects.get(pk=course_id)
            print(course)
            serializer=CourseSerializer(course)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'fetching data faild'},status=status.HTTP_400_BAD_REQUEST)
class AddChapter(APIView):
    def post(self,request):
        try:
            course_id=request.data.get('course_id')
            chaptername=request.data.get('chapterName')
            description=request.data.get('description')
            videos=request.data.get('videos')
            print('-------------><-------------')
            course=Course.objects.get(pk=course_id)
            Chapter.objects.create(
                course=course,
                videos=videos,
                description=description,
                chapter=chaptername
            )
            return Response({'message':'success the add course'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'add chapter fails'},status=status.HTTP_400_BAD_REQUEST)

class FetchChapter(APIView):
    def get(self,request):
        try:
            print('==============>>')
            course_id=request.query_params.get('id')
            print('--------------->/',course_id)
            course=Course.objects.get(pk=course_id)
            print(course)
            chapters=Chapter.objects.filter(course=course)
            print(chapters)
            serializer=ChapterSerilizer(chapters,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'fetching data faild'},status=status.HTTP_400_BAD_REQUEST)

class CourseCompleted(APIView):
    def put(self,request):
        try:
            course_id=request.data.get('id')
            print(course_id)
            course=Course.objects.get(pk=course_id)
            course.is_completed=True
            course.save()
            return Response({'message':'course completed success '},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'course completed faild'},status=status.HTTP_400_BAD_REQUEST)

class CourseCompletedList(APIView):
    def get(self,request):
        try:
            teacher_id=request.query_params.get('user_id')
            teacher=CustomUser.objects.get(pk=teacher_id)
            course=Course.objects.filter(instructor=teacher,is_completed=True)
            serializer=CourseSerializer(course,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':e},status=status.HTTP_400_BAD_REQUEST)
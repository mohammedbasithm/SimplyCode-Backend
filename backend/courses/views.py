from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category,Course,Chapter
from rest_framework.response import Response
from .serializers import CategorySerializer,CourseSerializer,ChapterSerilizer
from authentification.models import CustomUser
from rest_framework import status
from payments.models import Payments
from payments.serializer import PaymentSerializer

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
import json
class AddChapter(APIView):
    def post(self,request):
        try:
            course_id=request.data.get('course_id')
            chaptername=request.data.get('chapterName')
            description=request.data.get('description')
            videos=request.data.get('videos')
            is_free=request.data.get('is_free')
            print('-------------><-------------',json.loads(is_free))
            course=Course.objects.get(pk=course_id)
            Chapter.objects.create(
                course=course,
                videos=videos,
                description=description,
                chapter=chaptername,
                is_free=json.loads(is_free)
            )
            return Response({'message':'success the add course'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'add chapter fails'},status=status.HTTP_400_BAD_REQUEST)

class FetchChapter(APIView):
    def get(self,request):
        try:
            print('==============>>')
            course_id=request.query_params.get('courseId')
            print('--------------->/',course_id)
            course=Course.objects.get(pk=course_id)
            
            chapters=Chapter.objects.filter(course=course)
            
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
        
class FetchPaymentData(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            course_id = request.query_params.get('course_id')

            print('course:', course_id, ', user:', user_id)
            course = Course.objects.get(pk=course_id)
            user = CustomUser.objects.get(pk=user_id)
            print(course)
            print('user:', user)
            
            # Fetch a single payment object
            payment_data = Payments.objects.get(course=course, user=user)
            
            # Serialize the single payment object
            serializer = PaymentSerializer(payment_data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Payments.DoesNotExist:
            return Response({'error': 'Payment data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print('Error:', e)
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

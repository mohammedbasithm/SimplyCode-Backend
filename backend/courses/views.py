from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category,Course,Chapter
from rest_framework.response import Response
from .serializers import CategorySerializer,CourseSerializer,ChapterSerilizer
from authentification.models import CustomUser
from rest_framework import status
from payments.models import Payments
from payments.serializer import PaymentSerializer
from django.db.models import Count
import json

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
            user_id=request.data.get('user_id')

            teacher=CustomUser.objects.get(pk=user_id)
            Course.objects.create(
                title=courseName,
                category=category,
                description=description,
                instructor=teacher,
                price=price,
                cover_image=coverimage,
                about=about
            )
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

            user=CustomUser.objects.get(pk=user_id)
            course=Course.objects.filter(instructor=user,is_completed=False)
           
            serializer=CourseSerializer(course,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class CourseDetails(APIView):
    def get(self,request):
        try:
            course_id=request.query_params.get('id')
            
            course=Course.objects.get(pk=course_id)
            
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
            is_free=request.data.get('is_free')
            
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
            course_id=request.query_params.get('courseId')
            
            course=Course.objects.get(pk=course_id)  
            chapters=Chapter.objects.filter(course=course)
            
            serializer=ChapterSerilizer(chapters,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':'fetching data faild'},status=status.HTTP_400_BAD_REQUEST)

class CourseCompleted(APIView):
    def put(self,request):
        try:
            course_id=request.data.get('id')
            
            course=Course.objects.get(pk=course_id)

            course.is_completed=True
            course.save()

            return Response({'message':'course completed success '},status=status.HTTP_200_OK)
        except Exception as e:
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

            course = Course.objects.get(pk=course_id)
            user = CustomUser.objects.get(pk=user_id)
            payment_data = Payments.objects.get(course=course, user=user)
            
            serializer = PaymentSerializer(payment_data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Payments.DoesNotExist:
            return Response({'error': 'Payment data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PopularCourse(APIView):
    def get(self, request):
        try:
            successful_payments = Payments.objects.filter(status='success')
            course_purchases = successful_payments.values('course').annotate(total_purchases=Count('course'))
            sorted_courses = course_purchases.order_by('-total_purchases')
            most_purchased_courses_ids = [item['course'] for item in sorted_courses]

            # Retrieve the Course objects for the most purchased courses
            most_purchased_courses = Course.objects.filter(id__in=most_purchased_courses_ids,is_active=True)[:3]

            serializer = CourseSerializer(most_purchased_courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class EditCourse(APIView):
    def put(self,request):
        try:
            courseName=request.data.get('coursename')
            price=request.data.get('price')
            category_name=request.data.get('category')
            description=request.data.get('description')
            about=request.data.get('about')
            coverimage=request.data.get('coverimage')
            user_id=request.data.get('user_id')
            courseId=request.data.get('courseId')

            teacher=CustomUser.objects.get(pk=user_id)
            course=Course.objects.get(pk=courseId,instructor=teacher)
            categoryId=Category.objects.get(category=category_name)
            
            if course:
                course.title=courseName
                course.price=price
                course.category=categoryId
                course.description=description
                course.about=about
                course.cover_image=coverimage
                course.save()
                return Response({'message':'course updated success'},status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'message': 'Course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({'message': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Error updating course'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseDelete(APIView):
    def delete(self,request):
        try:
            courseId=request.query_params.get('courseId')
            teacherId=request.query_params.get('userId')

            teacher=CustomUser.objects.get(pk=teacherId)
            course=Course.objects.get(pk=courseId,instructor=teacher)
            
            if course:
                course.delete()
                return Response({'message': 'Course deleted successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'message': 'Course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Error deleting course'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
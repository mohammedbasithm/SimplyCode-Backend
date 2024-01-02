from django.shortcuts import render
from rest_framework.views import APIView
from authentification.models import *
from rest_framework.response import Response
from rest_framework import status
from .serilizers import UserListSerializers
from rest_framework.permissions import IsAuthenticated
from courses.models import Course
from courses.serializers import CourseSerializer

# Create your views here.
   
class UserProfile(APIView):
    def get(self,request):
        print("====================",request.data)
        user_id = request.query_params.get('user_id')
        print(user_id,'<--->')
        user=CustomUser.objects.get(pk=user_id)
        print(user_id,'<--->')
        serializer=UserListSerializers(user)
        print(user_id,'<--->')
        return Response(serializer.data,status=status.HTTP_200_OK)
class EditProfile(APIView):
    def put(self,request):
        user_id=request.data.get('user_id')
        print('----->',user_id)
        username=request.data.get('username')
        firstname=request.data.get('firstname')
        lastname=request.data.get('lastname')
        phone=request.data.get('phone')
        address=request.data.get('address')
        city=request.data.get('city')
        state=request.data.get('state')
        print('username:',username,'firstname:',firstname,'lastname:',lastname,'phone:',phone,'address:',address,'city:',city,'state:',state)
        user_obj=CustomUser.objects.get(pk=user_id)
        if CustomUser.objects.filter(username=username).exists():
            return Response({'message':'username is already taken please chose another name'},status=status.HTTP_200_OK)
        if username:
            print('username:',username)
            user_obj.username=username
        if firstname:
            user_obj.first_name=firstname
        if lastname:
            user_obj.last_name=lastname
        if phone:
            user_obj.phone=phone
        if address:
            user_obj.address=address
        if city:
            user_obj.city=city
        if state:
            user_obj.state=state
        print('-----------',user_obj)
        user_obj.save()
        
        return Response({'message':'success the changing your data'},status=status.HTTP_200_OK)
class EditProfileImg(APIView):
    def put(self,request):
        user_id=request.data.get('user_id')
        img_file=request.data.get('file')
        user=CustomUser.objects.get(pk=user_id)

        if img_file:
            user.image=img_file
            user.save()
        else:
            return Response({'message':'image file not found'},status=status.HTTP_200_OK)
        return Response({'message':'success the upload image'},status=status.HTTP_200_OK)

from django.contrib.auth.hashers import check_password
class CheckingTheCurrentPassword(APIView):
    def put(self,request):
        print("----->")
        user_id=request.data.get('user_id')
        print(user_id)
        current_pass=request.data.get('password')
        print(current_pass)
        user=CustomUser.objects.get(pk=user_id)
        print('helo---')
        if check_password(current_pass, user.password):
            return Response({'message':'success request'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'wrong the password'},status=status.HTTP_400_BAD_REQUEST)

class SetNewPassword(APIView):
    def post(self,request):
        user_id=request.data.get('user_id')
        password=request.data.get('password')

        user=CustomUser.objects.get(pk=user_id)
        if password:
            user.set_password(password)
            user.save()
        return Response({'success':'success the changing password'},status=status.HTTP_200_OK)
    
class FetchCourse(APIView):
    def get(self,request):
        try:
            courses=Course.objects.filter(is_completed=True).order_by('id')
            serializer=CourseSerializer(courses,many=True)
            print(serializer.data)
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
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class MyCourse(APIView):
    def get(self,request):
        try:
            print("))))))))))))))))0")
            user_id = request.query_params.get('user_id')
            print("+++++++++++",user_id)
            user=CustomUser.objects.get(pk=user_id)
            print('------->')
            mycourse=Course.objects.filter(
                payments__user_id=user_id,
                payments__status='success',
                payments__is_paid=True  
            ).distinct()
            print(mycourse)
            
            serializer=CourseSerializer(mycourse,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'error':'my course fetching faild'},status=status.HTTP_400_BAD_REQUEST)
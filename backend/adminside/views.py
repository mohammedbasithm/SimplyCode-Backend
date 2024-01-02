from django.shortcuts import render
from authentification.models import CustomUser
from rest_framework.views import APIView
from authentification.models import *
from rest_framework.response import Response
from rest_framework import status
from users.serilizers import UserListSerializers
from .serializers import CustomUserSerializer
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from courses.models import Course

# Create your views here.
class UserList(APIView):
    def get(self,request):
        userlist = CustomUser.objects.exclude(Q(is_superuser=True) | Q(approvel=True) | Q(is_teacher=True)).order_by('username')
        
        serializer=UserListSerializers(userlist, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class UserBlock(APIView):
    def put(self,request,user_id):
        try:
            user=CustomUser.objects.get(pk=user_id)
            print(user)
            user.is_active=False
            user.save()

            return Response({'message':'user blocked successfully'},status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserUnblock(APIView):
    
    # permission_classes=[IsAuthenticated,IsAdmin]
    def put(self,request,user_id):
        try:
            print("-------",request)
            user=CustomUser.objects.get(pk=user_id)
            print(user)
            user.is_active=True
            user.save()

            return Response({'message':'user unblock successfully'},status=status.HTTP_200_OK) 
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TeacherRequest(APIView):
    def get(self,request):
        print('hello....')
        teacher_request=CustomUser.objects.filter(teacher_request=True) 
        serializer=CustomUserSerializer(teacher_request,many=True)
        return Response({'teachers':serializer.data},status=status.HTTP_200_OK)

class TeacherApprovel(APIView):
    def put(self,request):
        try:
            print("----->")
            user_id=request.data.get('user_id')
            user=CustomUser.objects.get(pk=user_id)
            print(user)
            approvel=request.data.get('isApprovel')
            if approvel:
                print('hello')
                user.approvel=True
                user.teacher_request=False
                user.save()
                print('aaaaaaaaaaaaaaaa')
                serializer=CustomUserSerializer(user)

                #email confirmation for the user
                try:
                    #email confirmation for the user
                    send_mail(
                        f'Hi {user.username}',
                        'Congratulations! Your account has been successfully approved. You can now access our platform and start exploring our courses. Login to your account and begin your learning journey!',
        
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print('hello----')
                    print(f'Email sending error: {e}')


                return Response({'teacher':serializer.data,'message':'success the approvel'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'message':'somthing problem'},status=status.HTTP_400_BAD_REQUEST)

class TeacherReject(APIView):
    def put(self,request):
        try:
            teacher_id=request.data.get('id')
            print('teacher_id:',teacher_id)
            user=CustomUser.objects.get(pk=teacher_id)
            print(user)
            send_mail(
                f'Hi {user.username}',
                'We regret to inform you that your account approval request has been declined. Unfortunately, your application did not meet our current criteria. If you believe this decision is in error or would like more information, please contact our support team. Thank you for your interest in our platform.',

                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            user.delete()
            return Response({'message':'rejected successfully'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'rejected faild '},status=status.HTTP_400_BAD_REQUEST)

class TeacherList(APIView):
    def get(self,request):
        try:
            teacherData=CustomUser.objects.filter(approvel=True)
            serializer=CustomUserSerializer(teacherData,many=True)
            print(teacherData)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class TeacherBlock(APIView):
    def put(self,request):
        try:
            teacher_id=request.data.get('id')
            user=CustomUser.objects.get(pk=teacher_id)
            user.is_active=False
            user.save()
            return Response({'message':'teacher blocked success fully'},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'user not found '},status=status.HTTP_400_BAD_REQUEST)

class TeacherUnblock(APIView):
    def put(self,request):
        try:
            teacher_id=request.data.get('id')
            user=CustomUser.objects.get(pk=teacher_id)
            user.is_active=True
            user.save()
            return Response({'message':'teacher unblock success '},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'user not found '},status=status.HTTP_400_BAD_REQUEST)

class TeacherDetails(APIView):
    def get(self,request):
        try:
            print('------------')
            teacher_id=request.GET.get('id')
            print(teacher_id)
            teacherData=CustomUser.objects.get(pk=teacher_id)
            serializer=CustomUserSerializer(teacherData)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BlockCourse(APIView):
    def put(self,request):
        print("------------&& ")
        try:
            course_id=request.data.get('course_id')
            course=Course.objects.get(pk=course_id)
            course.is_active=False
            course.save()
            return Response({'message':'success the block course'},status=status.HTTP_200_OK)
        except:
            return Response({'error':'faild the block course'},status=status.HTTP_400_BAD_REQUEST)

class UnBlockCourse(APIView):
    def put(self,request):
        try:
            course_id=request.data.get('course_id')
            print('course_id:',course_id)
            course=Course.objects.get(pk=course_id)
            course.is_active=True
            course.save()
            return Response({'message':'success the unblock course'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response (status=status.HTTP_400_BAD_REQUEST)

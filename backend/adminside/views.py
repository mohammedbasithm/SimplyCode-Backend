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

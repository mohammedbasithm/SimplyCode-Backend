from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.utils.encoding import force_bytes , force_str
from .Token import generate_token
from django.core.mail import send_mail , EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseRedirect


class HomeView(APIView):
     
    
    def get(self, request):
        content = {'message': 'Welcome to the JWT  Authentication page using React Js and Django!'}
        return Response(content)

class CustomTokenObtainPairView(TokenObtainPairView):
    print('1----------')
    serializer_class = CustomTokenObtainPairSerializer
    print('2-2---------')
    def post(self, request, *args, **kwargs):
        print('3----------')
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data['username']
            user = CustomUser.objects.get(username=username)
            
            print('4----------',username)
            response.data['username'] = username
            response.data['uid']=user.pk
            response.data['is_active']=user.is_active
            response.data['is_admin']=user.is_superuser
            response.data['is_teacher']=user.is_teacher
            response.data['is_approvel']=user.approvel
            response.data['teacher_request']=user.teacher_request
            print('hiiiii')
            
        return response
    
class RegisterView(APIView):
    def post(self,request):
        try:
            username=request.data.get('username')
            email=request.data.get('email')
            password=request.data.get('password')
            is_teacher=request.data.get('is_teacher')
            print(username)
            print(email)
            print('hei')
            print(password)
            if not (username and email and password):
                return Response({'message': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)
            print("----------------------")
            if CustomUser.objects.filter(username=username).exists() :
                print('helooooo')
                return Response({'message':'Usre name already exist'},status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(email=email).exists():
                return Response({'message':'email already exist'},status=status.HTTP_400_BAD_REQUEST)
            print("-----2-----------------")
            # Create a new user object
            teacher = is_teacher.lower() == 'true'
            myuser=CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_teacher=teacher
                )
            print(myuser)
            myuser.is_active=True
            myuser.save()
            print('***********')
            #email confirmation for the user
            current_site=get_current_site(request)
            print("++++++++")
            email_subject = 'confirm Your email @ Simply code'
            print("++++++++")
            message2=render_to_string('activation_mail.html',{
                'name': myuser.username ,
                'domain': current_site.domain ,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })
            myuser.email_user(email_subject,message2)
            
            # print(')))))))))))))')
            # email = EmailMessage(
            #     email_subject,message2,
            #     settings.EMAIL_HOST_USER,
            #     [myuser.email] 
            # )
            # email.fail_silently = True
            # email.send()

            print("-----3-----------------")
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print("except error....")
            traceback.print_exc()
            # Handle exceptions here and return an appropriate error response
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class LogoutView(APIView):
    def post(self,request):
        try:
            print('log out')
            refresh_token=request.data.get('refresh_token')
            print('********',refresh_token)
            if not refresh_token:
                return Response({'message':'Refresh token missing'},status=status.HTTP_BAD_REQUEST)
            print('############')
            token=RefreshToken(refresh_token)
            print('&&&&&&&&&')
            token.blacklist()
            print('++++++++')
            return Response({'message':'Successfully logged out'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message':'Invalid token or an error occurred'},status=status.HTTP_400_BAD_REQUEST)

def activate(request,uidb64,token):
    print("pPPPPPPPPPPPp")
    try:
        print("pPPPPPPPPPPPp")
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=CustomUser.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser=None
      # checking the user and token doesnt has a conflict  
    if myuser is not None and generate_token.check_token(myuser,token):
        
        myuser.is_active=True
        print('kkkkkkkkkkkk')
        session=settings.SITE_URL + '/login'
     #    return render(request,'verification_success.html')
        if myuser.date_joined > timezone.now() - timedelta(hours=24):
            myuser.save()
        # myuser.save()
        return HttpResponseRedirect(session) 
    else:
        # Delete the user if activation fails and the activation link is expired
        user_creation_time = myuser.date_joined
        # Define the expiration time (24 hours after user creation)
        expiration_time = user_creation_time + timedelta(hours=24)  

        if myuser is not None and myuser.is_active == False and timezone.now() > expiration_time:
            myuser.delete()

        return render(request, 'verification_failed.html') 

class ForgotPasswordView(APIView):
    def post(self,request):
        try:
                
            email=request.data.get('email')
            print(',,,,,,,,>')
            myuser=CustomUser.objects.get(email=email)
            print(',,,,,,,,>')
            current_site=get_current_site(request)
            email_subject='Confirm Your Email for Password Reset'
            message2=render_to_string('forgot_password_mail.html',{
                'name':myuser.username,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token':generate_token.make_token(myuser)
            })
            email=EmailMessage(
                email_subject,message2,
                settings.EMAIL_HOST_USER,
                [myuser.email]
            )
            email.fail_silently=True
            email.send()

            return Response({'message':'email sent successfully '},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def forgot_password_mail_view(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        print(uidb64)
        print(uid)
        myuser=CustomUser.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        session = settings.SITE_URL + '/login/?uidb64=' + uidb64
        return HttpResponseRedirect(session) 

class ResentPassword(APIView):
    def post(self,request):
        print('---------')
        password=request.data.get('password')
        uidb64=request.data.get('uidb64')
        # uid=force_str(urlsafe_base64_decode(uidb64))
        # print(uidb64)
        # print(uid)
        print(password)
        print(uidb64)
        if isinstance(uidb64, str):
            
            try:
                print('---3------')
                uid=force_str(urlsafe_base64_decode(uidb64))
                print('---------')
                myuser=CustomUser.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError, User.DoesNotExist):
                myuser=None
            if myuser is not None:
                myuser.set_password(password)
                myuser.save()
                
                return Response({'message':'Password rest successfully'},status=200)
            else:
                return Response({"error":'Invalid or expires reset link'},status=400)
        else:
            return Response({'error': 'Invalid uidb64 type'}, status=400)


        
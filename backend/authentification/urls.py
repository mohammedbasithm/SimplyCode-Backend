from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('signup',RegisterView.as_view(),name='signup'),
    path('token', 
        CustomTokenObtainPairView.as_view(), 
        name ='token_obtain_pair'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('activate/<uidb64>/<token>', views.activate ,name='activate'),
    path('forgot-password',ForgotPasswordView.as_view(),name='forgot-password'),
    path('resend_password_mail/<uidb64>/<token>',views.forgot_password_mail_view,name='resend_password_mail'),
    path('reset-password',ResentPassword.as_view(),name='reset-password'),

]   
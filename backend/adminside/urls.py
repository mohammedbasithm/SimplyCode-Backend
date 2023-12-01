from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('userlist',UserList.as_view(),name='user-list'),
    path('blockuser/<int:user_id>/',UserBlock.as_view(),name='block-user'),
    path('userunblock/<int:user_id>/',UserUnblock.as_view(),name='user-unblock'),
    path('teacher-request',TeacherRequest.as_view(),name='teacher-request'),
    path('teacher-approvel',TeacherApprovel.as_view(),name='teacher-approvel'),
]
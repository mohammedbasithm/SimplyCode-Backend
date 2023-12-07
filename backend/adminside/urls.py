from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('userlist',UserList.as_view(),name='user-list'),
    path('blockuser/<int:user_id>/',UserBlock.as_view(),name='block-user'),
    path('userunblock/<int:user_id>/',UserUnblock.as_view(),name='user-unblock'),
    path('teacher-request',TeacherRequest.as_view(),name='teacher-request'),
    path('teacher-approvel',TeacherApprovel.as_view(),name='teacher-approvel'),
    path('teacher-reject',TeacherReject.as_view(),name='teacher-reject'),
    path('teacherlist',TeacherList.as_view(),name='teacher-list'),
    path('teacher-block',TeacherBlock.as_view(),name='teacher-block'),
    path('teacher-unblock',TeacherUnblock.as_view(),name='teacher-unblock'),
    path('teacherdetails',TeacherDetails.as_view(),name='teacher-details'),
]
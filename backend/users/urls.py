from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('profildetails',UserProfile.as_view(),name='profile-details'),
    path('editprofile',EditProfile.as_view(),name='edit-profile'),
    path('profileimg',EditProfileImg.as_view(),name="edit-profileimg"),
    path('current-password',CheckingTheCurrentPassword.as_view(),name='current-pass'),
    path('setnew-password',SetNewPassword.as_view(),name='setnew-pass'),
    path('user/fetchcourse',FetchCourse.as_view(),name='fetchcourse'),
    path('user/coursedetails',CourseDetails.as_view(),name='coursedetails'),
    path('user/mycourse',MyCourse.as_view()),
]   

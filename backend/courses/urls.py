from django.urls import path
from . import views
from .views import *

urlpatterns = [
    
     path('addcourse',AddCourse.as_view(),name='addcourse'),
     path('category',FetchCategory.as_view(),name='fetch-category'),
     path('listcourse',ListCourse.as_view(),name='list-course'),
     path('coursedetails',CourseDetails.as_view(),name='coursedetails'),
     path('addchapter',AddChapter.as_view(),name='addchapter'),
     path('fetchchapter',FetchChapter.as_view(),name='fetchchapter'),
]
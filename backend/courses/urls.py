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
     path('course-completed',CourseCompleted.as_view(),name="course-completed"),
     path('coures-completedlist',CourseCompletedList.as_view(),name='runningclass'),
     path('fetchpaymentsData',FetchPaymentData.as_view()),
     path('popular-course',PopularCourse.as_view(),name='popular-course'),
     path('editcourse',EditCourse.as_view(),name='edit-course'),
     path('course-delete',CourseDelete.as_view(),name='delete-course'),
]
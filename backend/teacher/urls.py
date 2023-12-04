from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('additional-details',AdditionDetailsTeacher.as_view(),name='teacher-details'),
]
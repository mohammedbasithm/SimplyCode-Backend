from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('user/blog',FetchBlog.as_view(),name='fetch-block'),
    path('blog/addcomment',AddComment.as_view(),name='add-comment'),
    path('blog/fetchcomment',FetchComment.as_view(),name='fetch-comment'),
    path('teacher/createblog',AddBlog.as_view(),name='create-blog'),
    path('teacher/blogdetails',BlogDetails.as_view(),name='blog-details'),
    path('blogdelete',BlogDelete.as_view(),name='blog-delete'),
]   
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BlogPost,Comments,Like
from .serializer import BlogPostSerializer,CommentsSerializer
from rest_framework import status
from authentification.models import CustomUser

# Create your views here.
class FetchBlog(APIView):
    def get(self,request):
        block_data=BlogPost.objects.all().order_by('-id')
        serializer=BlogPostSerializer(block_data,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AddComment(APIView):
    def post(self,request):
        try:
            blogId=request.data.get('blog_id')
            userId=request.data.get('user_id')
            comment=request.data.get('inputComment')
            print('comment:',comment)
            print('blogId:',blogId,'   userid:',userId)
            blog=BlogPost.objects.get(pk=blogId)
            user=CustomUser.objects.get(pk=userId)
            Comments.objects.create(
                blog_post=blog,
                user=user,
                content=comment
            )
            return Response({"message":"add comment success"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"add comment faild"},status=status.HTTP_400_BAD_REQUEST)
        
class FetchComment(APIView):
    def get(self,request):
        try:
            blogId=request.query_params.get('blogId')
            blog=BlogPost.objects.get(pk=blogId)
            print('blogs:',blog)
            comment=Comments.objects.filter(blog_post=blog)
            serializer=CommentsSerializer(comment,many=True)
            print(serializer.data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AddBlog(APIView):
    def post(self,request):
        try:
            content=request.data.get('content')
            title=request.data.get('title')
            thumanil=request.data.get('thumnail')
            teacherId=request.data.get('userId')

            teacher=CustomUser.objects.get(pk=teacherId)

            BlogPost.objects.create(
                title=title,
                content=content,
                author=teacher,
                image=thumanil
            )
            return Response({'message':'add blog successed'},status=status.HTTP_200_OK)
        except:
            return Response({"error":"add blog faild"},status=status.HTTP_400_BAD_REQUEST)

class BlogDetails(APIView):
    def get(self,request):
        try:
            userId=request.query_params.get('user_id')
            blogId=request.query_params.get('id')
            print('userId:',userId)
            print('blogid:',blogId)
            user=CustomUser.objects.get(pk=userId)
            blog=BlogPost.objects.filter(author=user,pk=blogId)
            serializer=BlogPostSerializer(blog,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BlogDelete(APIView):
    def get(self, request):
        try:
            userId = request.query_params.get('user_id')
            blogId = request.query_params.get('blog_id')
            
            user = CustomUser.objects.get(pk=userId)
           
            blog = BlogPost.objects.get(pk=blogId, author=user)
            blog.delete()
            return Response({'message':'blog deleted success'},status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


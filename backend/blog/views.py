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
            comment=Comments.objects.filter(blog_post=blog)
            
            serializer=CommentsSerializer(comment,many=True)
            
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
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
            
            user=CustomUser.objects.get(pk=userId)
            blog=BlogPost.objects.filter(author=user,pk=blogId)
            serializer=BlogPostSerializer(blog,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
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

class EditBlogDetails(APIView):
    def post(self, request):
        try:
            title = request.data.get('title')
            content = request.data.get('content')
            image = request.data.get('thumbnail')
            teacher_id = request.data.get('teacher_id')
            blog_id = request.data.get('blog_id')

            teacher = CustomUser.objects.get(pk=teacher_id)
            blog = BlogPost.objects.get(pk=blog_id, author=teacher)

            if blog:
                blog.title = title
                blog.content = content
                blog.image = image
                blog.save()

                return Response({'message': 'Data updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserBlogdetails(APIView):
    def get(self,request):
        try:
            blogId=request.query_params.get('blogId')
            blogData=BlogPost.objects.get(pk=blogId)
            serializer=BlogPostSerializer(blogData)
            likecount=Like.objects.all().count()

            return Response({'data':serializer.data,'likecount':likecount},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BlogLike(APIView):
    def get(self,request):
        try:
            blogId=request.query_params.get('blogId')
            userId=request.query_params.get('userId')
            like=request.query_params.get('like')

            blog=BlogPost.objects.get(pk=blogId)
            user=CustomUser.objects.get(pk=userId)

            if Like.objects.filter(user=user,blog_post=blog).exists():
                data=Like.objects.get(user=user,blog_post=blog)
                data.delete()
            else:
                Like.objects.create(
                    blog_post=blog,
                    user=user
                )
            likeCount=Like.objects.all().count()
            return Response({likeCount},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

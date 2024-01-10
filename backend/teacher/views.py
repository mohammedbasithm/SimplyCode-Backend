from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from authentification.models import CustomUser
from rest_framework import status
from users.serilizers import UserListSerializers
from authentification.serializers import CustomUserSerializer
from blog.models import BlogPost
from blog.serializer import BlogPostSerializer


# Create your views here.
class AdditionDetailsTeacher(APIView):
    def post(self, request):
        try:
            id = request.data.get("user_id")

            user = CustomUser.objects.get(pk=id)

            phone = request.data.get("phone")
            qualification = request.data.get("qualification")
            bank_account = request.data.get("bankaccount")
            ifsc = request.data.get("ifsc")
            id_proof = request.data.get("idproof")
            certificate = request.data.get("certificate")

            errors = []

            if not phone or not phone.strip():
                errors.append("Phone number is required")

            if not qualification or not qualification.strip():
                errors.append("Qualification is required")

            if not bank_account or not bank_account.strip():
                errors.append("Bank account number is required")

            if not ifsc or not ifsc.strip():
                errors.append("IFSC code is required")

            if not id_proof:
                errors.append("ID proof file is required")

            if not certificate:
                errors.append("Certificate file is required")

            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            if user:
                user.phone = phone
                user.qualification = qualification
                user.bank_account_number = bank_account
                user.ifsc_code = ifsc
                user.id_proof = id_proof
                user.certificate = certificate
                user.teacher_request = True
                try:
                    user.save()
                except Exception as e:
                    return Response(
                        {"errors": "Error during save"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                serializer = UserListSerializers(user)

                return Response(
                    {
                        "teacher": serializer.data,
                        "message": "Data Submission Successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"errors": "User not found"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception:
            return Response(
                {"errors": "somthing problems"}, status=status.HTTP_400_BAD_REQUEST
            )


class TeacherData(APIView):
    def get(self, request):
        try:
            teacher_id = request.query_params.get("teacherId")

            teacher = CustomUser.objects.get(pk=teacher_id)

            serializer = CustomUserSerializer(teacher)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)


class FetchBlogData(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get("userId")

            author = CustomUser.objects.get(pk=user_id)
            blog = BlogPost.objects.filter(author=author).order_by("-id")

            serializer = BlogPostSerializer(blog, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

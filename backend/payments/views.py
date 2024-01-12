from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import stripe
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from courses.models import Course
from .models import Payments
from django.urls import reverse
from authentification.models import CustomUser
from chat.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

stripe.api_key =settings.STRIPE_SECRET_KEY

@method_decorator(csrf_exempt, name='dispatch')
class StripeCheckoutView(APIView):
    def post(self, request):
        course_id=request.data.get('id')
        user_id=request.data.get('user_id')
        
        course=Course.objects.get(pk=course_id)
        user=CustomUser.objects.get(pk=user_id)
        
        default_price = 0 
        unit_amount_paise = int(course.price * 100) if course.price is not None else default_price
        course_image="https://www.hackhackathon.com/ImagesGallery/AdminImageGallery/imagePath/2021-04-21-04-27-5-tips-to-learn-coding-with-no-prior-experience.png"

        try:
            request.session['stripe_user_id']=user_id
            request.session['stripe_course_id']=course_id
            request.session.save()
            print(f"Session contents after saving: {request.session.items()}")
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': course.title,
                                'images': [course_image],
                            },
                             'unit_amount': unit_amount_paise,
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card', ],
                mode='payment',
                # success_url=settings.SITE_URL + '/success/?success=true&session_id={CHECKOUT_SESSION_ID}',
                success_url = f"http://127.0.0.1:8000/api/stripe/success-checkout/?success=true&session_id={{CHECKOUT_SESSION_ID}}&course_id={course_id}&user_id={user_id}",
                cancel_url=settings.SITE_URL+'/?canceled=true',
                metadata={'course_id': course_id, 'user_id': user_id},
            )
            # payment=Payments.objects.create(
            #     course=course,
            #     user=user,
            #     teacher=course.instructor,
            #     amount=course.price,
            #     status='success',
            #     is_paid=True
                
            # )
            # if payment.status=='success':
            #     group, created = Group.objects.get_or_create(
            #         course=course,
            #         title=f"{course.title} Community",
            #         description="Discussion and collaboration for this course."
            #     )
            #     group.members.add(user)
            #     course.is_subscripe=True
            #     course.save()
            print('8888888888888')
            response_data = {'checkout_session_url': checkout_session.url}
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({'error': 'Something went wrong when creating a stripe checkout session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SuccessCheckOut(APIView):
    def get(self,request):
        try:
            print('----------------->')
            
            course_id = request.query_params.get('course_id')
            user_id = request.query_params.get('user_id')
            print(f'course_id: {course_id}')
            print(f'user_id: {user_id}')
            course=Course.objects.get(pk=course_id)
            user=CustomUser.objects.get(pk=user_id)

            payment=Payments.objects.create(
                course=course,
                user=user,
                teacher=course.instructor,
                amount=course.price,
                status='success',
                is_paid=True
                
            )
            if payment.status=='success':
                group, created = Group.objects.get_or_create(
                    course=course,
                    title=f"{course.title} Community",
                    description="Discussion and collaboration for this course."
                )
                group.members.add(user)
                course.is_subscripe=True
                course.save()
            
            
            success_url = f"{settings.SITE_URL}/success/?success=true&session_id={{CHECKOUT_SESSION_ID}}"
            return redirect(success_url)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
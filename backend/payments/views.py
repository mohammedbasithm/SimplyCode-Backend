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

stripe.api_key =settings.STRIPE_SECRET_KEY
class StripeCheckoutView(APIView):
    def post(self, request):
        course_id=request.data.get('id')
        user_id=request.data.get('user_id')
        course=Course.objects.get(pk=course_id)
        user=CustomUser.objects.get(pk=user_id)
        
        default_price = 0  # Provide a default price if course.price is missing
        unit_amount_paise = int(course.price * 100) if course.price is not None else default_price
        course_image="https://www.hackhackathon.com/ImagesGallery/AdminImageGallery/imagePath/2021-04-21-04-27-5-tips-to-learn-coding-with-no-prior-experience.png"
        # course_image = "http://127.0.0.1:8000/course.cover_image"

        try:
            print('hello..')
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
                success_url=settings.SITE_URL + '/success/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL+'/?canceled=true',
            )
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

            print(f"Checkout Session URL: {checkout_session.url}")
            response_data = {'checkout_session_url': checkout_session.url}
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            # Log or print the specific error message
            print(f"Stripe Error: {e}")
            return Response({'error': 'Something went wrong when creating a stripe checkout session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Log or print the specific error message
            print(f"Error: {e}")
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

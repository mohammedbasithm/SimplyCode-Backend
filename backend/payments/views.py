from django.shortcuts import render
from django.conf import settings
import stripe
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status

stripe.api_key =settings.STRIPE_SECRET_KEY
from django.urls import reverse

class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            print('hello..9')
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': 'basith',
                            },
                             'unit_amount': 999,
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card', ],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL+'/?canceled=true',
            )
            print(f"Checkout Session URL: {checkout_session.url}")
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            # Log or print the specific error message
            print(f"Stripe Error: {e}")
            return Response({'error': 'Something went wrong when creating a stripe checkout session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Log or print the specific error message
            print(f"Error: {e}")
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

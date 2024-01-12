from django.urls import path
from .views import StripeCheckoutView,StripeWebhookView

urlpatterns = [
   path('create-checkout-session',StripeCheckoutView.as_view()),
   path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
   
]
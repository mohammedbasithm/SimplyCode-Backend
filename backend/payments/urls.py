from django.urls import path
from .views import StripeCheckoutView,SuccessCheckOut

urlpatterns = [
   path('create-checkout-session',StripeCheckoutView.as_view()),
   path('success-checkout',SuccessCheckOut.as_view(),name='success_checkout'),
   
]
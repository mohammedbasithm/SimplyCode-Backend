from django.urls import path
from .views import*

urlpatterns = [
    path('chat/fetchRoom',FetchChatRoom.as_view(),name='fetch-room'),
    path('chat/fetchMessage',FetchMessage.as_view(),name='fetchMessage'),
]
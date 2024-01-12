from django.urls import path
from .views import*

urlpatterns = [
    path('chat/fetchRoom',FetchChatRoom.as_view(),name='fetch-room'),
    path('chat/fetchMessage',FetchMessage.as_view(),name='fetchMessage'),
    path('userName',GetUsername.as_view(), name='get_username'),
    path('chat/save-message',SaveMessage.as_view(),name='save-message'),
]
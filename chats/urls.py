from django.urls import path, re_path


from .views import (ChatThreadCreateAPIView, ChatThreadDetailAPIView, DetailedChatMessageAPIView,
ChatMessageAPIView, CreateCallAPIView, ChatListAPIView, CallListAPIView)


app_name = 'chat-api'
urlpatterns = [
    path('chat-list/', ChatListAPIView.as_view(), name='chat-list'),
    path('call-list/', CallListAPIView.as_view(), name='call-list'),
    re_path(r"^(?P<pk>[\d+-]+)/call/$",
            CreateCallAPIView.as_view(), name='call'),

    re_path(r"^(?P<pk>[\d+-]+)/$",
            ChatThreadCreateAPIView.as_view(), name='chat'),

    re_path(r"^thread/(?P<pk>[\d+-]+)/details/$",
            ChatThreadDetailAPIView.as_view(), name='chat-detail'),

    re_path(r"^(?P<pk>[\d+-]+)/messages/$",
            ChatMessageAPIView.as_view(), name='chat-message'),

    re_path(r"^message/(?P<pk>[\d-]+)/details/$",
            DetailedChatMessageAPIView.as_view(), name='detail-chat'),

]

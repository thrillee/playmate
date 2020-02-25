from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.response import Response

from accounts.auth import TokenAuthentication
from accounts.models import PlayMateUser
from accounts.permissions import IsOwnerOrReadOnly, UserInThread

from .models import ChatMessage, Thread, ChatList, Call, CallList
from .serializers import (ChatMessageSerializer,
ThreadSerializer, ChatListSerialzier, CallSerializer, CallListSerializer)


class ChatThreadCreateAPIView(generics.CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        try:
            serializer.save(
                first=self.request.user,
                second=PlayMateUser.objects.get(
                    id=self.kwargs.get('pk')))
        except:
            return Reponse({
                "status": False,
                "detail": "Second user not found"
            })


class ChatThreadDetailAPIView(generics.RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [UserInThread]
    authentication_classes = (TokenAuthentication,)


#Have to setup Paginator for this
class ChatMessageAPIView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        thread, created=Thread.objects.get_or_new(
            self.request.user, self.kwargs['pk'])
        return ChatMessage.objects.filter(thread=thread)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, thread=Thread.objects.get_or_new(
            self.request.user, self.kwargs['pk'])[0])


class DetailedChatMessageAPIView(generics.RetrieveDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [UserInThread]
    authentication_classes = (TokenAuthentication,)

    def perform_destory(self, instance):
        instance.delete()


class CreateCallAPIView(generics.CreateAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    permission_classes = [UserInThread]
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        thread=Thread.objects.get_or_new(
                            self.request.user, self.kwargs.get('pk'))[0])


class ChatListAPIView(generics.ListAPIView):
    serializer_class = ChatListSerialzier
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return ChatList.objects.filter(user=self.request.user)


class CallListAPIView(generics.ListAPIView):
    serializer_class = CallListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return CallList.objects.filter(user=self.request.user)

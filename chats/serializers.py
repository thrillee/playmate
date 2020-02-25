from rest_framework import serializers

from accounts.serializers import UserProfileSerializer
from accounts.models import PlayMateUser

from .models import ChatMessage, Thread, ChatList, Call, CallList


class UserSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)

    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PlayMateUser
        fields = ('id', 'owner', 'phone_number', 'first_name', 'last_name',
                  'email', 'profile')

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj == request.user:
                return True
            return False
        return False

    def get_profile(self, obj):
        return UserProfileSerializer(obj.user_profile, read_only=True).data


class ThreadSerializer(serializers.ModelSerializer):
    first = UserSerializer(read_only=True)
    second = UserSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    thread = ThreadSerializer(read_only=True)
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ChatListMessage(serializers.ModelSerializer):
    thread = ThreadSerializer(read_only=True)
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ChatListSerialzier(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    message = ChatListMessage(read_only=True)
    class Meta:
        model = ChatList
        fields = '__all__'


class CallSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Call
        fields = "__all__"


class CallListSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    call = CallSerializer(read_only=True)
    class Meta:
        model = CallList
        fields = '__all__'

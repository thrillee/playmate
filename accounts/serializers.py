from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import PhoneOTP, PlayMateUser, Profile


class ProfileUserSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PlayMateUser
        fields = ('id', 'owner', 'phone_number', 'first_name', 'last_name',
                  'email', 'is_active', 'last_login', 'date_joined')

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj == request.user:
                return True
            return False
        return False


class ProfileSerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
    


class UserSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    update = serializers.HyperlinkedIdentityField(
        view_name='accounts:user-update',
        lookup_field='pk'
    )
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PlayMateUser
        fields = ('id', 'owner', 'phone_number', 'first_name', 'last_name',
        'email', 'is_active', 'last_login', 'date_joined', 'update',
        'profile')

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj == request.user:
                return True
            return False
        return False

    def get_profile(self, obj):
        return UserProfileSerializer(obj.user_profile, read_only=True).data


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if phone_number and otp:

            user = PlayMateUser.objects.filter(phone_number=phone_number)
            if user.exists():
                user = user.first()
                user.otp = otp
                user.save()
                data['user'] = user
                return data
            else:
                msg = {
                    'status': False,
                    'detail': 'User does not exist.',
                }

                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = {
                'status': False,
                'detail': 'Phone number and OTP not found',
            }
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayMateUser
        fields = ('id', 'phone_number', 'otp')
    
    def create(self, validated_data):
        user, created = PlayMateUser.objects.create_user(**validated_data)
        if created:
            user.set_unusable_password()
            user.save()
        return user, created

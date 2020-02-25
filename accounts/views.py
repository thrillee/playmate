import time
from random import randint

from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import permissions, status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from knox.views import LoginView as KnoxLoginView

from .auth import TokenAuthentication
from .models import PhoneOTP, PlayMateUser, PmAuthToken, Profile
from .permissions import IsUserOrReadOnly
from .serializers import (LoginSerializer, RegisterSerializer, UserSerializer, ProfileSerializer)


class RegisterPhone(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', False)
        if phone_number:
            old = PhoneOTP.objects.filter(phone_number__iexact=phone_number)
            if old.exists():
                old = old.last()
                old.used = True
                old.save()
                
            otp, sent = send_otp(str(phone_number))
            if sent:
                print(otp)
                return Response({
                    'status': True,
                    'detail': f'OTP sent to {phone_number}'
                })

            return HttpResponseBadRequest('Error in sending OTP', 
        content_type="application/json")
 
        return HttpResponseBadRequest('Provide phone number or action (register or login)', 
        content_type="application/json")



def send_otp(phone):
    if phone:
        token = str("%06d" % randint(0, 999999))
        PhoneOTP.objects.create(phone_number=phone, otp=token)
        """ some sending stuff will takeoff here """
        return token, True
    return False


class LoginAPI(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        
        phone_number = request.data.get('phone_number', False)
        otp_sent = request.data.get('otp', False)

        if phone_number and otp_sent:
            old = PhoneOTP.objects.filter(phone_number__iexact=phone_number)
            if old.exists():

                old = old.last()
                otp = old.otp

                if old.expiry >= timezone.now():
                    if str(otp_sent) == str(otp):
                        old.validated = True

                        user = PlayMateUser.objects.filter(
                            phone_number__iexact=phone_number)
                        if not old.used:
                            old.used = True
                            old.save()
                            if user.exists():
                                login_serializer = self.get_serializer(data=request.data)
                                login_serializer.is_valid(raise_exception=True)
                                user = login_serializer.validated_data['user']
                                if user:
                                    instance, token = PmAuthToken.objects.create(user)
                                    user_logged_in.send(sender=PlayMateUser, request=request, user=user)
                                    login(request, user)
                                    
                                    return Response({
                                        'user': UserSerializer(user, context=self.get_serializer_context()).data,
                                        'token': token
                                    })
                            return HttpResponseBadRequest('User does not exist.', 
                            content_type="application/json") 
                        return HttpResponseBadRequest('OTP is used.', 
                            content_type="application/json") 
                    return HttpResponseBadRequest('Incorrect OTP.', 
                            content_type="application/json") 
                return HttpResponseBadRequest('Expired OTP.', 
                            content_type="application/json") 
            return HttpResponseBadRequest('OTP does not exist.', 
                            content_type="application/json")
        return HttpResponseBadRequest('Missing phone number or OTP.', 
                            content_type="application/json")


class RegisterUserAPI(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', False)
        otp_sent = request.data.get('otp', False)
        
        if phone_number and otp_sent:
            old = PhoneOTP.objects.filter(phone_number__iexact=phone_number)
            if old.exists():
                old = old.last()
                otp = old.otp

                if old.expiry >= timezone.now():
                    if str(otp_sent) == str(otp):
                        old.validated = True
                        if not old.used:
                            
                            register_serializer = self.get_serializer(data=request.data)
                            register_serializer.is_valid(raise_exception=True)
                            user, created = register_serializer.save()
                            old.used = True
                            old.save()
                            if created:
                                instance, token = PmAuthToken.objects.create(
                                    user)
                                user_logged_in.send(
                                    sender=PlayMateUser, request=request, user=user)
                                print(phone_number, otp_sent)
                                login(request, user)
                                return Response({
                                    'user': UserSerializer(user, context=self.get_serializer_context()).data,
                                    'token': token
                                })
                            return HttpResponseBadRequest('OTP is used.', 
                            content_type="application/json") 
                        return HttpResponseBadRequest('User can not be created.', 
                            content_type="application/json")  
                    return HttpResponseBadRequest('Incorrect OTP.', 
                            content_type="application/json") 
                return HttpResponseBadRequest('Expired OTP.', 
                            content_type="application/json")
            return HttpResponseBadRequest('OTP does not exist.', 
                            content_type="application/json")
        return HttpResponseBadRequest('Missing phone number or OTP.', 
                            content_type="application/json") 


class GetUser(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return [self.request.user]


class PlayMateUsers(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PlayMateUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'profile__display_name')



class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserUpdateAPI(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = PlayMateUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly, permissions.IsAuthenticated)
    

    def perform_update(self, serializer):
        return serializer.save(is_active=True)


class ProfileUpdateAPI(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsUserOrReadOnly, permissions.IsAuthenticated)
    
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)
    

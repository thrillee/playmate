from django.urls import path, re_path
from .views import (RegisterPhone, LoginAPI, RegisterUserAPI, 
LogoutView, UserUpdateAPI, ProfileUpdateAPI, GetUser)
from knox import views as knox_views


app_name = 'accounts'
urlpatterns = [
    path('user/', GetUser.as_view()),
    path('validate-phone/', RegisterPhone.as_view(), name='validate-phone'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('register/', RegisterUserAPI.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    re_path(r'^user/(?P<pk>[\d-]+)/update/$',
            UserUpdateAPI.as_view(), name='user-update'),
    re_path(r'^profile/(?P<pk>[\d-]+)/update/$',
            ProfileUpdateAPI.as_view(), name='profile-update'),
]

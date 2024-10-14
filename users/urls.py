"""
This module contains the URL configuration for the users app.
"""
from django.urls import path

from users.views import creator_views, auth_views, otp_views

app_name = 'users'

creator_auth_urls = [
    path('signup/creator/', creator_views.CreatorSignUpView.as_view(), name='creator_signup'),
]

otp_urls = [
    path('auth/otp/verify/<uuid:user_id>/', otp_views.OTPVerificationView.as_view(), name='verify_otp'),
    path('auth/otp/resend/<uuid:user_id>/', otp_views.ResendOTPView.as_view(), name='resend_otp'),
]

auth_urls = [
    path('auth/login/', auth_views.LoginView.as_view(), name='login'),
    path('auth/logout/', auth_views.LogOutView.as_view(), name='logout'),
]

urlpatterns = creator_auth_urls + otp_urls + auth_urls

from django.urls import path
from .views import SendOtp, VerifyOtp


urlpatterns = [
        path('send_otp/', SendOtp.as_view(), name='send_otp'),
        path('verify_otp/', VerifyOtp.as_view(), name='verify_otp'),
]
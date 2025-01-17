from django.urls import path
from .views import SendOtp, VerifyOtp, UserProfileView, UserListView


urlpatterns = [
        path('send_otp/', SendOtp.as_view(), name='send_otp'),
        path('verify_otp/', VerifyOtp.as_view(), name='verify_otp'),
        path('user_list/', UserListView.as_view(), name="user_list"),
        path('profile/', UserProfileView.as_view(), name='profile'),
]
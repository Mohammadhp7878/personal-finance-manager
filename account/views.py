import logging
import requests
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from .serializers import (
    UserPhoneSerializer,
    UserProfileSerializer,
    CustomUserSerializer,
)
from .models import CustomUser, UserProfile
from .permissions import IsOwner
from rest_framework import generics
from utils import generate_otp, verify_otp

logger = logging.getLogger(__name__)
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    summary="Send OTP to a phone number",
    description="Send a one-time password (OTP) to the provided phone number.",
    request=UserPhoneSerializer,
    responses={
        200: OpenApiTypes.OBJECT,  
        400: OpenApiTypes.OBJECT, 
    },
)
class SendOtp(APIView):
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = UserPhoneSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            phone = serializer.validated_data["phone"]
        except ValidationError as e:
            logger.warning(f"failed to verify phone because of {e}")
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        otp = generate_otp(phone)
        headers = {
            "apiKey": settings.MSG_API_KEY,
            "accept-language": "fa",
            "Content-Type": "application/json",
        }
        body = {
            "mobile": phone,
            "method": "sms",
            "templateID": 3,
            "length": 6,
            "code": str(otp),
        }
        response = requests.post(
            "https://api.msgway.com/send", headers=headers, data=json.dumps(body)
        )
        if response.status_code == 200:
            request.session["phone"] = phone
            logger.info(f"otp send successfully to user with {phone} number")
            return Response(
                {"message": "code sent successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"error": "something went wrong! try again"},
            status=status.HTTP_400_BAD_REQUEST,
        )




@extend_schema(
    summary="Verify OTP and authenticate the user",
    description="Verify the OTP code sent to the user and return access and refresh tokens upon successful verification.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "otp": {"type": "string", "example": "123456"},
            },
            "required": ["otp"],
        }
    },
    responses={
        200: OpenApiTypes.OBJECT,  
        400: OpenApiTypes.OBJECT,  
    },
)
class VerifyOtp(APIView):
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        phone = request.session.get("phone")
        enterd_otp = request.data.get("otp")

        if not enterd_otp or not phone:
            return Response(
                {"error": "phone and otp code are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            verify_otp(phone, enterd_otp)
            user, created = CustomUser.objects.get_or_create(phone=phone)

            request.session.flush()

            refresh = RefreshToken.for_user(user)
            logger.info(f"user with {phone} phone number logged in successfully")

            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            logger.warning(f"failed to send OTP because of {e}")
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner]

    def get_object(self):
        return self.request.user.user_profile
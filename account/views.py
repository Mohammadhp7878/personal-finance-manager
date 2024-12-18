import logging
import requests
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from .serializers import UserPhoneSerializer
from utils import generate_otp

logger = logging.getLogger(__name__)


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



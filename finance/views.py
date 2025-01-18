from rest_framework.views import APIView
from .serializers import CryptoAssetSerializer
from .models import CryptoAsset
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CryptoAssetView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CryptoAssetSerializer(data=request.data, context={"user": request.user})
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        crypto_data = CryptoAsset.objects.filter(user=request.user)
        serialized_data = CryptoAssetSerializer(crypto_data, many=True)  
        try:
            return Response(serialized_data.data)
        except ValidationError as e:
            return Response({'errors': str(e)})
        


class SingleCryptoView(APIView):
    ...

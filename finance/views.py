from rest_framework import generics
from .serializers import CryptoAssetSerializer
from .models import CryptoAsset


class AddCryptoAsset(generics.CreateAPIView):
    serializer_class = CryptoAssetSerializer
    model = CryptoAsset

from rest_framework import generics
from .serializers import CryptoAssetSerializer
from .models import CryptoAsset
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status


class CryptoAssetView(generics.ListCreateAPIView):
    serializer_class = CryptoAssetSerializer
    queryset = CryptoAsset.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response("this coin already exists", status=status.HTTP_400_BAD_REQUEST)


class SingleCryptoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CryptoAssetSerializer
    lookup_field = "name"
    
    def get_queryset(self):
        return CryptoAsset.objects.filter(name=self.kwargs["name"])

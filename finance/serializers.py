from rest_framework import serializers
from .models import CryptoAsset
from cryptoFetcher import CryptoPriceFetcher


class CryptoAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAsset
        fields = ["name", "balance"]


    def create(self, validated_data):
        name = validated_data["name"]
        balance = validated_data["balance"]
        
        crypto_fetcher = CryptoPriceFetcher()
        crypto_data = crypto_fetcher.get_crypto_prices_by_id(name)
        id = crypto_data.keys()
        
        
        
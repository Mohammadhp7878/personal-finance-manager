from rest_framework import serializers
from .models import CryptoAsset
from cryptoFetcher import CryptoPriceFetcher
from rest_framework.validators import ValidationError

class CryptoAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAsset
        fields = ["name", "balance", "symbol", "price_at_purchase"]
        extra_kwargs = {
            "price_at_purchase": {"read_only": True},
        }


    def create(self, validated_data):
        name = validated_data["name"]
        balance = validated_data["balance"]
        crypto_fetcher = CryptoPriceFetcher() 
        id, slug, symbol = crypto_fetcher.get_crytpo_id(name)
        price = crypto_fetcher.get_crypto_price_by_id(str(id))
        
        crypto_asset = CryptoAsset.objects.create(name=slug, balance=balance, id=id, symbol=symbol, price_at_purchase=price)

        return crypto_asset
        
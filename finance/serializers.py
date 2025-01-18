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


    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["user"] = self.context.get("user")
        return data

    def create(self, validated_data, *args, **kwargs):
        user = validated_data["user"]
        name = validated_data["name"]
        balance = validated_data["balance"]
        crypto_fetcher = CryptoPriceFetcher() 
        coin_id, slug, symbol = crypto_fetcher.get_crytpo_id(name)
        price = crypto_fetcher.get_crypto_price_by_id(str(id))
        
        crypto_asset = CryptoAsset.objects.create(user=user, name=slug, balance=balance, coin_id=coin_id, symbol=symbol,
                                                  price_at_purchase=price)

        return crypto_asset
        
from django.db import models
from core.models import BaseModel
from account.models import CustomUser

class CryptoAsset(BaseModel):
    user = models.ForeignKey(CustomUser, related_name="crypto_assets", on_delete=models.CASCADE)
    coin_id = models.IntegerField(blank=True)
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    balance = models.DecimalField(decimal_places=2, max_digits=12)
    price_at_purchase = models.DecimalField(decimal_places=6, max_digits=12)
    
    
    class Meta:
        unique_together = (("user", "name"))

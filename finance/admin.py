from django.contrib import admin
from .models import CryptoAsset


@admin.register(CryptoAsset)
class CryptoAssetAdmin(admin.ModelAdmin):
    list_display = ["user__phone", "name", "symbol", "balance"]

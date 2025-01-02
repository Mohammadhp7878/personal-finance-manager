from django.urls import path
from .views import CryptoAssetView


urlpatterns = [
    path('add_crypto/', CryptoAssetView.as_view(), name="add_crypto"),
]
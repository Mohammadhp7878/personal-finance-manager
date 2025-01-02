from django.urls import path
from .views import CryptoAssetView, SingleCryptoView


urlpatterns = [
    path('add_crypto/', CryptoAssetView.as_view(), name="add_crypto"),
    path('crypto/<slug:name>', SingleCryptoView.as_view(), name="single_crypto")
]
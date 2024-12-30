from django.urls import path
from .views import AddCryptoAsset


urlpatterns = [
    path('add_crypto/', AddCryptoAsset.as_view(), name="add_crypto"),
]
import requests
from decouple import config
from rest_framework.validators import ValidationError
from rest_framework import status

class CryptoPriceFetcher:
    crypto_info = {}
    def __init__(self, currency="USD"):
        self.currency = currency
        self.base_url = "https://pro-api.coinmarketcap.com/v1/"
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": config("api_key_crypto"),
        }

    def get_crytpo_id(self, slug:str):
        url = f"{self.base_url}cryptocurrency/map"
        response = requests.get(url=url, headers=self.headers)
        data = response.json()
        crypto_id = None
        crypto_slug = None
        crypto_symbol = None
        for crypto in data["data"]:
            if crypto["slug"] == slug:
                crypto_id = crypto["id"]
                crypto_slug = crypto["slug"]
                crypto_symbol = crypto["symbol"]
                break
        if not crypto_id:
            raise ValidationError("This coin does not exist!", code=status.HTTP_404_NOT_FOUND)
        return crypto_id, crypto_slug, crypto_symbol

    def get_crypto_price_by_id(self, id:str):
        url = f"{self.base_url}cryptocurrency/quotes/latest"
        params = {"id":id, "convert":self.currency}
        response = requests.get(url=url, headers=self.headers, params=params)
        data = response.json()
        crypto_price =  data["data"][id]["quote"][self.currency]["price"]
        return crypto_price
        
        
        



# class CryptoPriceFetcher:
#     crypto_info = {}
#     def __init__(self, currency="USD"):
#         self.currency = currency
#         self.base_url = "https://pro-api.coinmarketcap.com/v1/"
#         self.headers = {
#             "Accepts": "application/json",
#             "X-CMC_PRO_API_KEY": config("api_key_crypto"),
#         }

#     def get_crytpo_id(self, slug:str):
#         url = f"{self.base_url}cryptocurrency/map"
#         response = requests.get(url=url, headers=self.headers)
#         data = response.json()

#         for crypto in data["data"]:
#             if crypto["slug"] == slug:
#                 crypto_id = crypto["id"]
#                 crypto_slug = crypto["slug"]
#                 crypto_symbol = crypto["symbol"]
        
#         return crypto_id, crypto_slug, crypto_symbol

#     def get_crypto_price_by_id(self, id:str):
#         url = f"{self.base_url}cryptocurrency/quotes/latest"
#         params = {"id":id, "convert":self.currency}
#         response = requests.get(url=url, headers=self.headers, params=params)
#         data = response.json()
#         crypto_price =  data["data"][id]["quote"][self.currency]["price"]
#         return crypto_price


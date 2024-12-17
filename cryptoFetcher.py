import requests
from decouple import config


class CryptoPriceFetcher:
    crypto_info = {}
    def __init__(self, currency="USD"):
        self.currency = currency
        self.base_url = "https://pro-api.coinmarketcap.com/v1/"
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": config("api_key_crypto"),
        }

    def get_crytpo_ids(self, slugs):
        url = f"{self.base_url}cryptocurrency/map"
        response = requests.get(url=url, headers=self.headers)
        data = response.json()
        crypto_info = {
            str(crypto["id"]): [crypto["slug"], crypto["symbol"]]
            for crypto in data["data"]
            if crypto["slug"] in slugs
        }
        return crypto_info

    def get_crypto_prices_by_id(self, slugs):
        url = f"{self.base_url}cryptocurrency/quotes/latest"
        crypto_info = self.get_crytpo_ids(slugs)
        ids = list(map(str, crypto_info.keys()))
        params = {"id":f"{",".join(ids)}", "convert":self.currency}
        response = requests.get(url=url, headers=self.headers, params=params)
        data = response.json()
        for id in ids:
            if id in ids:
                crypto_info[id].append(data["data"][id]["quote"][self.currency]["price"])
            else:
                crypto_info[id].append(None)
        return crypto_info
        


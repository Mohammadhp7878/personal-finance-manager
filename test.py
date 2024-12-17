import requests
from decouple import config


def get_crypto_ids(slugs:list):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
    headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': config("api_key_crypto"),
              }
    response = requests.get(url=url,headers=headers) 
    data = response.json()
    slug_to_id = {
            crypto["id"]: [crypto["slug"], crypto["symbol"]]
            for crypto in data["data"]
            if crypto["slug"] in slugs
            }
    return slug_to_id


def get_prices_by_id(crypto_info:dict):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    ids = list(map(str, crypto_info.keys()))
    params = {"id": f"{",".join(ids)}"}
    headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config("api_key_crypto"),
    }
    respnse = requests.get(url=url, headers=headers, params=params)
    data = respnse.json()
    data = [data["data"][id]["quote"]["USD"]["price"] for id in ids]
    print(data)
    
    
    
crypto_names = ["toncoin","notcoin"]
crypto_data = get_crypto_ids(slugs=crypto_names)
get_prices_by_id(crypto_data)




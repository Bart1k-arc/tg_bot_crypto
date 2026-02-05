import requests
import json
from confing import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException("Нельзя переводить одинаковые валюты.")

        if base not in keys:
            raise APIException(f"Валюта '{base}' не найдена.")

        if quote not in keys:
            raise APIException(f"Валюта '{quote}' не найдена.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество должно быть числом.")

        base_ticker = keys[base]
        quote_ticker = keys[quote]

        if base_ticker == "BTC":
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "bitcoin",
                "vs_currencies": quote_ticker.lower()
            }

            response = requests.get(url, params=params)
            data = response.json()

            rate = data["bitcoin"][quote_ticker.lower()]
            return rate * amount

        url = f"https://api.exchangerate-api.com/v4/latest/{base_ticker}"
        response = requests.get(url)

        data = json.loads(response.content)

        if "rates" not in data:
            raise APIException("API не вернул курсы валют.")

        rate = data["rates"][quote_ticker]

        return rate * amount

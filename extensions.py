import requests
import json
from config import CURRENCIES


class APIException(Exception):
    pass


class CurrencyConvector():
    @staticmethod
    def get_price(a_base: str, a_quote: str, a_amount: str) -> float:

        try:
            base_ticker = CURRENCIES[a_base]
        except KeyError:
            raise APIException(f"неизвестная валюта {a_base}")

        try:
            quote_ticker = CURRENCIES[a_quote]
        except KeyError:
            raise APIException(f"неизвестная валюта {a_quote}")

        if a_quote == a_base:
            raise APIException("Валюты не должны совпадать")

        try:
            a = float(a_amount)
        except:
            raise APIException(f"Количество валюты '{a_amount}' должно являться числом")

        request = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        exch_rate = json.loads(request.content)[CURRENCIES[a_quote]]
        return exch_rate * float(a_amount)

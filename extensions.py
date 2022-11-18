import json
import requests
from setting import value


class APIException(Exception):
    pass


class ConvertCurrency(APIException):
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты: {value[base]}')

        try:
            base_tag = value[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        try:
            quote_tag = value[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_tag}&tsyms={quote_tag}')
        res = json.loads(r.content)[quote_tag] * amount

        return res

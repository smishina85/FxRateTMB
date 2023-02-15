import requests
import json
from config import keys
from config import API_KEY


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'It is impossible to convert equal currencies {base}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Failed to process the base currency {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Failed to process the quoted currency {quote}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Failed to process the amount {amount}!')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_ticker}/{quote_ticker}')

# This will return the exchange rate from your base code to the other currency you supplied:
        #
        # {
        # 	"result": "success",
        # 	"documentation": "https://www.exchangerate-api.com/docs",
        # 	"terms_of_use": "https://www.exchangerate-api.com/terms",
        # 	"time_last_update_unix": 1585267200,
        # 	"time_last_update_utc": "Fri, 27 Mar 2020 00:00:00 +0000",
        # 	"time_next_update_unix": 1585270800,
        # 	"time_next_update_utc": "Sat, 28 Mar 2020 01:00:00 +0000",
        # 	"base_code": "EUR",
        # 	"target_code": "GBP",
        # 	"conversion_rate": 0.8412
        # }
        fx_rate = str(round(json.loads(r.content)['conversion_rate'], 3) * amount)
        return fx_rate





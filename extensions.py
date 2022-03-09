import requests
import json
from config import keys

# Класс исключений
class APIExeption(Exception):
    pass
# Класс конвертера
class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):# метод конвертации валюты
        # quote, base, amount = message.text.split(' ')
        if quote == base:# проверка на одинаковость валют
            raise APIExeption(f'Одинаковая валюта {base}, сумма не изменилась: {amount}')
        # проверка на наличие валют
        try:
            quote_ticker = keys[quote]
            # print(quote_ticker)
        except KeyError:
            raise APIExeption(f'В списке нет валюты {quote}')

        try:
            base_ticker = keys[base]
            # print(base_ticker)
        except KeyError:
            raise APIExeption(f'В списке нет валюты {base}')
        # проверка на правильность суммы
        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество {amount}')
        # отправка запроса и возвращение результата
        request_string = f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}'
        # print(request_string)
        r = requests.get(request_string)
        total_base = json.loads(r.content)[keys[quote]]
        # print(total_base)
        return total_base
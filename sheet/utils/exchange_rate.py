from xml.etree import ElementTree

import requests

USD_EXCHANGE_RATE = None
URL_FOR_RATE = "http://www.cbr.ru/scripts/XML_daily.asp"


def get_usd_exchange_rate():
    global USD_EXCHANGE_RATE

    if USD_EXCHANGE_RATE is None:
        update_usd_exchange_rate()

    return USD_EXCHANGE_RATE


def update_usd_exchange_rate():
    global USD_EXCHANGE_RATE

    response = requests.get(URL_FOR_RATE)

    if response.status_code == 200:
        root = ElementTree.fromstring(response.content)
        for valute in root.findall("Valute"):
            if valute.find("CharCode").text == "USD":
                usd_exchange_rate = float(
                    valute.find("Value").text.replace(",", "."))
                USD_EXCHANGE_RATE = usd_exchange_rate
                return
    else:
        raise ValueError("Не удалось получить курс доллара")

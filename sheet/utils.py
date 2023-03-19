import logging
import os
import pickle
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import requests
from xml.etree import ElementTree

from UnwindDigitalTask.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from sheet.models import Order

USD_EXCHANGE_RATE = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_orders_due():
    orders = Order.objects.filter(delivery_date__lt=datetime.now().date())
    due_orders = []

    for order in orders:
        due_orders.append(order)
        logger.info(f"Срок поставки заказа {order.order_number} истек")

    return due_orders

def send_telegram_notification(due_orders):
    if not due_orders:
        return

    message = "Уведомление о просроченных заказах:\n\n"
    for order in due_orders:
        message += f"Номер заказа: {order.order_number}\nДата поставки: {order.delivery_date}\n\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
    response = requests.get(url)

    if response.status_code == 200:
        logger.info("Уведомление о просроченных заказах отправлено в Telegram")
    else:
        logger.error(f"Ошибка при отправке уведомления в Telegram: {response.status_code} - {response.text}")

def get_usd_exchange_rate():
    global USD_EXCHANGE_RATE

    if USD_EXCHANGE_RATE is None:
        update_usd_exchange_rate()

    return USD_EXCHANGE_RATE


def update_usd_exchange_rate():
    global USD_EXCHANGE_RATE

    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)

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


def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                ['https://www.googleapis.com/auth/spreadsheets'])
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_google_sheet(sheet_id, sheet_range):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=sheet_range
    ).execute()
    return result.get('values', [])


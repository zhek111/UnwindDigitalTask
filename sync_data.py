import os

import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnwindDigitalTask.settings")
django.setup()

from sheet.utils import setup_logger

import time
from datetime import datetime

from googleapiclient.errors import HttpError

from sheet.models import Order
from sheet.utils import get_google_sheet, get_usd_exchange_rate

SHEET_ID = '1aGov-wMHdqfshgmO6qogOrw9uwqDuvM2cpOkcl33Y3M'
SHEET_RANGE = 'Лист1!A2:E'
SLEEP_INTERVAL = 60  # время между проверками обновления таблицы, в секундах

logger = setup_logger(__name__)


def update_orders(data):
    existing_orders = {
        order.order_number: order for order in Order.objects.all()
    }
    usd_exchange_rate = get_usd_exchange_rate()

    for row in data:
        order_number, cost, delivery_date = int(row[1]), float(
            row[2]), datetime.strptime(row[3], '%d.%m.%Y').date()
        cost_rub = cost * usd_exchange_rate
        if order_number in existing_orders:
            order = existing_orders[order_number]
            order.cost = cost
            order.delivery_date = delivery_date
            order.cost_rub = cost_rub
            order.save()
            del existing_orders[order_number]
        else:
            Order.objects.create(order_number=order_number, cost=cost,
                                 delivery_date=delivery_date,
                                 cost_rub=cost_rub)

    # удаление заказов, которые больше не существуют в таблице
    for order in existing_orders.values():
        order.delete()


if __name__ == "__main__":

    while True:
        try:
            sheet_data = get_google_sheet(SHEET_ID, SHEET_RANGE)
            if sheet_data:
                update_orders(sheet_data)
            time.sleep(SLEEP_INTERVAL)
        except HttpError as error:
            logger.error(f"Произошла ошибка: {error}")
            time.sleep(SLEEP_INTERVAL)

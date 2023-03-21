from celery import shared_task

from sheet.utils import update_usd_exchange_rate
from sheet.utils import check_orders_due
from sheet.utils import send_telegram_notification


@shared_task
def update_usd_exchange_rate_task():
    update_usd_exchange_rate()


@shared_task
def check_and_notify_due_orders():
    due_orders = check_orders_due()
    send_telegram_notification(due_orders)

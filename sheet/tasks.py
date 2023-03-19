from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .utils import update_usd_exchange_rate, check_orders_due, \
    send_telegram_notification


@shared_task
def update_usd_exchange_rate_task():
    update_usd_exchange_rate()


@shared_task
def check_and_notify_due_orders():
    due_orders = check_orders_due()
    send_telegram_notification(due_orders)
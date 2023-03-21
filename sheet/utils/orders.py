from datetime import datetime

from sheet.models import Order
from sheet.utils.logging import setup_logger

logger = setup_logger(__name__)


def check_orders_due():
    orders = Order.objects.filter(delivery_date__lt=datetime.now().date())
    due_orders = []

    for order in orders:
        due_orders.append(order)
        logger.info(f"Срок поставки заказа {order.order_number} истек")

    return due_orders

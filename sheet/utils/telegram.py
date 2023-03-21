import requests

from sheet.utils.logging import setup_logger
from UnwindDigitalTask.settings import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN

logger = setup_logger(__name__)


def send_telegram_notification(due_orders):
    if not due_orders:
        return

    message = "Уведомление о просроченных заказах:\n\n"
    for order in due_orders:
        message += f"Номер заказа: {order.order_number}\nДата поставки: " \
                   f"{order.delivery_date}\n\n"

    url = f"https://api.teleg" \
          f"ram.org/bot{TELEGRAM_TOKEN}/sendMessage?ch" \
          f"at_id={TELEGRAM_CHAT_ID}&text={message}"
    response = requests.get(url)

    if response.status_code == 200:
        logger.info("Уведомление о просроченных заказах отправлено в Telegram")
    else:
        logger.error(
            f"Ошибка при отправке уведомления в Telegram: "
            f"{response.status_code} - {response.text}")

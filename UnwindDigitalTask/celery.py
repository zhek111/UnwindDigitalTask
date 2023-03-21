import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UnwindDigitalTask.settings')

app = Celery('UnwindDigitalTask')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_usd_exchange_rate': {
        'task': 'sheet.tasks.update_usd_exchange_rate_task',
        'schedule': crontab(minute=0, hour=12, day_of_week='mon-fri'),
    },
    'check_and_notify_due_orders': {
        'task': 'sheet.tasks.check_and_notify_due_orders',
        'schedule': crontab(minute=0, hour=9, day_of_week='mon-fri'),
    },
}

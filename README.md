# Orders
Orders это Django-приложение, которое автоматически синхронизирует данные из Google-таблицы с заказами и сохраняет их в базе данных. Оно также использует Celery для выполнения периодических задач, таких как обновление курса доллара и отправка уведомлений о просроченных заказах через Telegram.
## Установка и настройка
1. Клонируйте репозиторий:
```bash
$ git clone https://github.com/zhek111/python-project-52/
```
2. Установите и активируйте виртуальное окружение:
3. Установите зависимости:
```bash
$ pip install -r requirements.txt
```
4. Получите `credentials.json` из Google API. Следуйте инструкциям в [официальной документации Google](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the_api_name) для получения файла `credentials.json`. Поместите этот файл в корневую папку проекта.
5. Создайте .env файл в корневой директории и добавьте переменный из envsample
6. Запустите Redis
7. Выполните миграции:
```bash
$ python manage.py migrate
```
6. Запустите сервер:
```bash
$ python manage.py runserver
```
7. Запустите Celery:
```bash
$ make celery
```
8. Запустите скрипт для синхронизации данных из Google-таблицы:
```bash
$ make script
```

## Основные API

- `/api/orders/` - список всех заказов с возможностью создания нового заказа.

## Celery задачи

- `update_usd_exchange_rate` - обновление курса доллара каждый рабочий день в 12:00.
- `check_and_notify_due_orders` - проверка просроченных заказов и отправка уведомлений в Telegram каждый рабочий день в 9:00.

## Использование

После запуска сервера разработки и Celery, приложение будет автоматически синхронизировать данные из Google-таблицы с заказами и сохранять их в базе данных. Вы можете использовать предоставленные API-маршруты для работы с заказами и просмотра их статуса. Если у вас есть просроченные заказы, вы получите уведомление в Telegram.

## Technologies Used
* Django
* Django REST Framework
* PostgreSQL
* Celery
* Redis
* Google API


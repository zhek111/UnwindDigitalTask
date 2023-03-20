install:
	pip install -r requirements.txt

start:
	python manage.py runserver

script:
	python sync_data.py

celery:
	celery -A UnwindDigitalTask worker --loglevel=info --detach
	celery -A UnwindDigitalTask beat --loglevel=info --detach




import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cowin.settings')

app = Celery('cowin')

app.config_from_object('cowin.celeryconfig')
app.autodiscover_tasks()

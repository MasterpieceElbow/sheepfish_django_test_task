import os
from celery import Celery
from decouple import config


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sheep_fish_task.settings")

app = Celery("sheep_fish_task")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.broker_url = os.getenv("BROKER_URL", "redis://0.0.0.0:6379")

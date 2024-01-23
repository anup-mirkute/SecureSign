from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SecureSign.settings')


# Create a Celery instance and configure it using the settings from Django
celery_app = Celery(['SecureSign'])


# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.broker_transport_options = {'result_backend': 'redis://127.0.0.1:6379/0'}


# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()


# Celery Scheduled Tasks
celery_app.conf.beat_schedule = {
    'delete_unverified_user': {
        'task': 'accounts.tasks.delete_unverified_user',  # Specify the path to your task
        'schedule': 10,
        # 'schedule': crontab(hour=24, minute=00),    # Schedule daily at 12 AM
    },
}
# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta  # Import timedelta for scheduling

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_dashboard.settings')

app = Celery('traffic_dashboard')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Set up the beat schedule for periodic tasks
app.conf.beat_schedule = {
    'update-sensors': {
        # Assuming your task is defined in a file called tasks.py in your backend app
        'task': 'backend.tasks.update_sensors',
        'schedule': timedelta(seconds=5),
    },
}

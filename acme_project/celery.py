from __future__ import absolute_import
from django.conf import settings
from celery import Celery
import os

# Configuration for celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acme_project.settings')

app = Celery('acme_project',broker='pyamqp://guest@localhost//')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ('acme_project',))

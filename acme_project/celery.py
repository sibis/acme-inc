from __future__ import absolute_import
from django.conf import settings
from celery import Celery
import os


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acme_project.settings')

app = Celery('acme_project',broker='pyamqp://guest@localhost//')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

#Now Celery will automatically discover tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ('acme_project',))


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
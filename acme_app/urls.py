from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from acme_app.views import upload_file, get_uploaded_file_status

urlpatterns = [
    url(r'^upload_file/$', upload_file, name='upload_file'),
    url(r'^list_uploaded_files/$', get_uploaded_file_status, name='get_uploaded_file_status'),
]
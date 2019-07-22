from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from acme_app.views import upload_file, get_uploaded_file_status, list_products, create_product, delete_products_info

urlpatterns = [
    url(r'^upload_file/$', upload_file, name='upload_file'),
    url(r'^list_uploaded_files/$', get_uploaded_file_status, name='get_uploaded_file_status'),
    url(r'^list_products/$', list_products, name='list_products'),
    url(r'^create_product/$', create_product, name='create_product'),
    url(r'^delete_products/$', delete_products_info, name='delete_products_info'),
]
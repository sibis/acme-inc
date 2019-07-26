from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/', include('authentication_app.urls')),
    url(r'^acme/', include('acme_app.urls')),
]

from django.conf.urls import url

from acme_app import consumers

websocket_urlpatterns = [
    url(r'^ws/notification/file_stream/$', consumers.StreamFileProcess),
]
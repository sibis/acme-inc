web: daphne acme_project.asgi:application --port $PORT --bind 0.0.0.0
worker: celery -A acme_project worker -B --loglevel=info  -E --concurrency=1

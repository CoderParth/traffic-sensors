release: python manage.py migrate --noinput
web: daphne traffic_dashboard.asgi:application --port $PORT --bind 0.0.0.0 -v2

release: python manage.py makemigrations && python manage.py migrate --noinput
web: gunicorn traffic_dashboard.wsgi --log-file -

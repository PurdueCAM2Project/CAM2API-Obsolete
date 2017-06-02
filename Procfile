web: python manage.py makemigrations
web: python manage.py migrate
web: python manage.py collectstatic --noinput
web: gunicorn API.wsgi --log-file -
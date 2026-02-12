#!/bin/bash
set -e

# run migrations then start the server
if [ "$RUN_MIGRATIONS" != "0" ]; then
  echo "Running migrations..."
  python manage.py migrate --noinput || true
fi

# create superuser if env set (useful for CI or dev automation)
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model();
if not User.objects.filter(username=\"$DJANGO_SUPERUSER_USERNAME\").exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
fi

exec "$@"

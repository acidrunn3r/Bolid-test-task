#!/bin/sh

echo "Waiting for database..."
while ! python - <<END
import psycopg2, os
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host="db"
    )
    conn.close()
except:
    exit(1)
END
do
  sleep 2
done

echo "Database ready. Applying migrations and collecting static..."
python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn bolid_backend.wsgi:application --bind 0.0.0.0:8000

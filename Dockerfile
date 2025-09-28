FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=bolid_backend.settings
ENV STATIC_ROOT=/app/staticfiles

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

#Basis-Image
FROM python:3.11.3-alpine

# Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere notwendige Abhängigkeiten
RUN apk add --no-cache \
  linux-headers \
  gcc \
  musl-dev \
  jpeg-dev \
  zlib-dev \
  mailcap

# Kopiere das Requirements in den Container
COPY requirements.txt /app/

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere das Django-Projekt in den Container
COPY . /app/

ENV DJANGO_CONFIGURATION=Production DJANGO_SETTINGS_MODULE=groceries.settings

# Exponiere den Port, auf dem das Django-Projekt läuft
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

ENV PYTHONUNBUFFERED=1
# Starte das Django-Projekt
CMD ["uwsgi", "-showconfig", "/app/uwsgi.ini"]

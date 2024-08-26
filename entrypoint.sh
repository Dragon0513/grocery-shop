#!/bin/sh
set -o errexit
set -o pipefail
set -o nounset

# Run database migrations
python manage.py migrate --noinput

# Collect static files (if needed)
python manage.py collectstatic --noinput

# Execute the command passed to the container
exec "$@"

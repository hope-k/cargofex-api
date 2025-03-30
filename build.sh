#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e # Add this line

# REMOVE the pip install line - Koyeb's buildpack should handle this.
# echo "Install Requirements..."
# pip install -r requirements.txt

echo "Apply Database Migrations..."
python manage.py migrate --noinput

echo "Create Superuser (if not exists)..."
# Ensure environment variables DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL,
# and DJANGO_SUPERUSER_PASSWORD are set in your Koyeb service settings!
python create_superuser.py # Make sure create_superuser.py is correct

echo "Collect Static..."
python manage.py collectstatic --noinput --clear

echo "Build finished successfully!"
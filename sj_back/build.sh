#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files with error handling
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear --verbosity=2 || {
    echo "Static files collection failed, trying without compression..."
    # Fallback: try collecting without compression
    STATICFILES_STORAGE=django.contrib.staticfiles.storage.StaticFilesStorage python manage.py collectstatic --no-input --clear
}

# Run migrations
echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"

# startup.sh - Script for Azure App Service startup

#!/bin/bash
echo "Starting Multi-Agent Research Web App..."

# Make sure gunicorn is installed
pip install gunicorn

# Start the application with gunicorn
exec gunicorn --bind=0.0.0.0:8000 web_app:app
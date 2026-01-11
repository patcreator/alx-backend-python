#!/bin/bash

# Create directory structure
mkdir -p Django-Middleware-0x03/chats
mkdir -p Django-Middleware-0x03/config
mkdir -p Django-Middleware-0x03/logs

echo "Project structure created successfully!"
echo "To get started:"
echo "1. cd Django-Middleware-0x03"
echo "2. python -m venv venv"
echo "3. source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "4. pip install -r requirements.txt"
echo "5. python manage.py migrate"
echo "6. python manage.py createsuperuser"
echo "7. python manage.py runserver"
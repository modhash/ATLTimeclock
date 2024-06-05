#!/bin/bash

echo "Updating system..."
sudo apt-get update -y

echo "Installing dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv sqlite3

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python packages..."
pip install -r backend/requirements.txt

echo "Initializing database..."
FLASK_APP=backend/app.py flask db init
FLASK_APP=backend/app.py flask db migrate
FLASK_APP=backend/app.py flask db upgrade

echo "Creating .env file..."
cat <<EOT >> .env
MICROSOFT_CLIENT_ID=YOUR_MICROSOFT_CLIENT_ID
MICROSOFT_CLIENT_SECRET=YOUR_MICROSOFT_CLIENT_SECRET
SECRET_KEY=YOUR_SECRET_KEY
EOT

echo "Starting the application..."
FLASK_APP=backend/app.py flask run

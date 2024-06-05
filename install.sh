#!/bin/bash

echo "Updating system..."
sudo apt-get update -y

echo "Installing system dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv sqlite3 build-essential libssl-dev libffi-dev python3-dev

echo "Setting up virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python packages..."
pip install -r backend/requirements.txt

echo "Initializing database..."
export FLASK_APP=backend/app.py
flask db init
flask db migrate
flask db upgrade

echo "Creating .env file..."
read -p "Enter your Microsoft Client ID: " microsoft_client_id
read -p "Enter your Microsoft Client Secret: " microsoft_client_secret
read -p "Enter your Flask Secret Key: " secret_key

cat <<EOT >> .env
MICROSOFT_CLIENT_ID=$microsoft_client_id
MICROSOFT_CLIENT_SECRET=$microsoft_client_secret
SECRET_KEY=$secret_key
EOT

echo "Creating admin user..."
read -p "Enter admin email: " admin_email
read -p "Enter admin username: " admin_username
read -sp "Enter admin password: " admin_password
echo

python3 <<PYTHON
from backend.models import db, User
from backend.app import app

with app.app_context():
    admin = User(email="$admin_email", username="$admin_username", is_admin=True)
    admin.set_password("$admin_password")
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
PYTHON

echo "Starting the application..."
export FLASK_APP=backend/app.py
flask run

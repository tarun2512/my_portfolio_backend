#!/bin/bash

# Change directory to the location of the script
cd "$(dirname "$0")"

# Deleting old app
sudo rm -rf /var/www/

# Creating app folder
sudo mkdir -p /var/www/my_portfolio_backend

# Moving files to app folder
sudo mv ./* /var/www/my_portfolio_backend/

# Navigate to the app directory
cd /var/www/my_portfolio_backend/

# Install pip and virtualenv if not already installed
sudo yum install python3-pip -y
sudo pip3 install virtualenv

# Create virtual environment
virtualenv venv

# Activate virtual environment
source venv/bin/activate

python3 --version

# Install application dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing application dependencies from requirements.txt"
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

# Change directory to the location of the script
cd "$(dirname "$0")"

# Create the directory if it doesn't exist
sudo mkdir -p /etc/nginx/conf.d/

# Configure Nginx as a reverse proxy
echo "Configuring Nginx as a reverse proxy"
sudo tee /etc/nginx/conf.d/myapp.conf > /dev/null <<EOF
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/my_portfolio_backend/myapp.sock;
    }
}
EOF

sudo nginx -t

sudo systemctl restart nginx

# Stop any existing Gunicorn process
echo "Stopping any existing Gunicorn process"
sudo pkill gunicorn
sudo rm -rf /var/www/my_portfolio_backend/myapp.sock

# Start Gunicorn with the Flask application
echo "Starting Gunicorn"
pip install gunicorn
sudo gunicorn --workers 3 --bind unix:/var/www/my_portfolio_backend/myapp.sock main:app --daemon
echo "Started Gunicorn 🚀"

# Deactivate the virtual environment
deactivate

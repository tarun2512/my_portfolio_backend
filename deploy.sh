#!/bin/bash

# Change directory to the location of the script
cd "$(dirname "$0")"

echo "Deleting old app"
sudo rm -rf /var/www/

echo "Creating app folder"
sudo mkdir -p /var/www/my_portfolio_backend

echo "Moving files to app folder"
sudo mv ./* /var/www/my_portfolio_backend/

# Navigate to the app directory
cd /var/www/my_portfolio_backend/

# Update package index and install necessary packages
echo "Updating package index and installing Python and pip"
sudo yum update -y
sudo yum install -y python3 python3-pip nginx

# Install application dependencies from requirements.txt
echo "Installing application dependencies from requirements.txt"
sudo pip3 install --user -r requirements.txt

# Configure Nginx as a reverse proxy
echo "Configuring Nginx as a reverse proxy"
sudo tee /etc/nginx/conf.d/myapp.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/my_portfolio_backend/myapp.sock;
    }
}
EOF

sudo systemctl restart nginx

# Stop any existing Gunicorn process
echo "Stopping any existing Gunicorn process"
sudo pkill gunicorn
sudo rm -rf myapp.sock

# Start Gunicorn with the Flask application
echo "Starting Gunicorn"
sudo pip3 install --user gunicorn
sudo gunicorn --workers 3 --bind unix:/var/www/my_portfolio_backend/myapp.sock main:app --user nginx --group nginx --daemon
echo "Started Gunicorn 🚀"

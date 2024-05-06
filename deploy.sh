#!/bin/bash

# Change directory to the location of the script
cd "$(dirname "$0")"

# Print current directory for debugging
echo "Current directory: $(pwd)"

# Deleting old app
sudo rm -rf /var/www/my_portfolio_backend/

# Creating app folder
sudo mkdir -p /var/www/my_portfolio_backend

# Moving files to app folder
sudo cp -r ./* /var/www/my_portfolio_backend/

# Navigate to the app directory
cd /var/www/my_portfolio_backend/

echo "Current directory: $(pwd)"

# Create and activate a virtual environment with appropriate permissions
sudo python3 -m venv venv

# Print virtual environment directory for debugging
ls -l venv

# Activate virtual environment
source venv/bin/activate

# Check if activation script is found
ls -l venv/bin/activate

sudo chmod -R u+rwx /var/www/my_portfolio_backend/

python3 --version

sudo pip install --upgrade pip

# Install application dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing application dependencies from requirements.txt"
    sudo pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

# Configure Nginx as a reverse proxy
echo "Configuring Nginx as a reverse proxy"
sudo tee /etc/nginx/conf.d/myapp.conf > /dev/null <<EOF
server {
    listen 80;
    server_name my_portfolio_backend;

    location / {
        proxy_pass http://unix:/var/www/my_portfolio_backend/myapp.sock;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo nginx -t
sudo systemctl start nginx

# Stop any existing Gunicorn process
echo "Stopping any existing Gunicorn process"
sudo pkill gunicorn
sudo rm -rf /var/www/my_portfolio_backend/myapp.sock

# Start Gunicorn with the Flask application
echo "Starting Gunicorn"
sudo pip install gunicorn
sudo gunicorn --workers 3 --bind unix:/var/www/my_portfolio_backend/myapp.sock main:app --daemon || { echo "Failed to start Gunicorn"; exit 1; }

echo "Started Gunicorn 🚀"

# Deactivate the virtual environment
deactivate || { echo "Failed to deactivate virtual environment"; exit 1; }

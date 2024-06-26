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

# Set permissions for the app folder
sudo chown -R $USER:$USER /var/www/my_portfolio_backend/
sudo chmod -R 755 /var/www/my_portfolio_backend/

# Remove existing virtual environment
rm -rf /var/www/my_portfolio_backend/venv/

# Create and activate a virtual environment
python3 -m venv venv/

# Activate virtual environment
source venv/bin/activate

# Upgrade pip within the virtual environment
python -m pip install --upgrade pip

# Install application dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing application dependencies from requirements.txt"
    pip install -r requirements.txt
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
        proxy_set_header Host "\$http_host";
        proxy_set_header X-Real-IP "\$remote_addr";
        proxy_set_header X-Forwarded-For "\$proxy_add_x_forwarded_for";
        proxy_set_header X-Forwarded-Proto "\$scheme";
    }
}
EOF

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl start nginx

# Stop any existing Gunicorn process
echo "Stopping any existing Gunicorn process"
pkill gunicorn
rm -f /var/www/my_portfolio_backend/myapp.sock

# Start Gunicorn with the Flask application
echo "Starting Gunicorn"
pip install gunicorn
gunicorn --workers 3 --bind unix:/var/www/my_portfolio_backend/myapp.sock main:app --daemon || { echo "Failed to start Gunicorn"; exit 1; }

echo "Started Gunicorn 🚀"

# Deactivate the virtual environment
deactivate || { echo "Failed to deactivate virtual environment"; exit 1; }

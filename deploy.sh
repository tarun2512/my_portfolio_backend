#!/bin/bash

# Change directory to the location of the script
cd "$(dirname "$0")"

echo "Deleting old app"
rm -rf /var/www/

echo "Creating app folder"
mkdir -p /var/www/my_portfolio_backend

echo "Moving files to app folder"
mv ./* /var/www/my_portfolio_backend/

# Navigate to the app directory
cd /var/www/my_portfolio_backend/

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install application dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing application dependencies from requirements.txt"
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

# Configure Nginx as a reverse proxy
echo "Configuring Nginx as a reverse proxy"
tee /etc/nginx/conf.d/myapp.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/my_portfolio_backend/myapp.sock;
    }
}
EOF

systemctl restart nginx

# Stop any existing Gunicorn process
echo "Stopping any existing Gunicorn process"
pkill gunicorn
rm -rf myapp.sock

# Start Gunicorn with the Flask application
echo "Starting Gunicorn"
pip install gunicorn
gunicorn --workers 3 --bind unix:/var/www/my_portfolio_backend/myapp.sock main:app --daemon
echo "Started Gunicorn 🚀"

# Deactivate the virtual environment
deactivate
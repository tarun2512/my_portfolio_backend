#!/bin/bash

# Update your application (replace with your actual commands)
sudo yum update -y

# Install additional dependencies if needed (replace with your package names)
# Example: sudo yum install -y package1 package2

# Replace with your deployment logic
# This section will vary depending on your application setup

# Option 1: Deploying a static website (replace with your directory)
# cp -r /path/to/your/local/website/* /var/www/html/

# Option 2: Deploying a Python application using virtual environment (replace with your details)
# Create virtual environment (if not already created)
 python3 -m venv my-env

# Activate virtual environment
 source my-env/bin/activate

# Clone/Pull your application code (replace with your Git repository URL)
 git clone https://github.com/<username>/<repository>.git my-app
 cd my-app
 git pull origin main

# Install application dependencies within the virtual environment
 pip install -r requirements.txt

# (Optional) Copy your application code to a specific directory on the EC2 instance
# cp -r ./* /var/www/html/my-app/  # Copies everything

# Create a systemd service file (replace with your app name and path)
 sudo nano /etc/systemd/system/my-app.service

# Example systemd service file content (adjust paths and commands):
 [Unit]
 Description=My Python App
 After=network.target

 [Service]
 WorkingDirectory=/var/www/html/my-app  # Replace with your app directory
 User=ec2-user
 Group=ec2-user
 Environment="PATH=/home/ec2-user/my-env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"  # Update path with virtual environment
 ExecStart=/home/ec2-user/my-env/bin/gunicorn wsgi:application -b 0.0.0.0:8000  # Update path with virtual environment

 [Install]
 WantedBy=multi-user.target

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl start my-app.service

# Enable the service to start automatically on boot
sudo systemctl enable my-app.service

# Deactivate the virtual environment (optional)
 deactivate

# (Optional) Restart any additional services (replace with your service names)
 sudo systemctl restart nginx  # Example for restarting nginx

# Let the script know it finished successfully
echo "Deployment completed!"

exit 0

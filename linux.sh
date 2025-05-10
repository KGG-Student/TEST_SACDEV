#!/bin/bash


# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Attempting to install..."
    sudo apt update && sudo apt install -y python3-pip
fi

# Create a requirements.txt file
cat <<EOF > requirements.txt
blinker==1.9.0
click==8.1.8
colorama==0.4.6
Flask==3.1.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
greenlet==3.2.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
SQLAlchemy==2.0.40
typing_extensions==4.13.2
Werkzeug==3.1.3
EOF

# Install the packages
pip3 install -r requirements.txt

echo "Installation complete."
#!/bin/bash

# Ensure required system packages are installed
sudo apt update
sudo apt install -y python3-venv python3-pip python3-full

# Create virtual environment if it doesn't exist
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created at $VENV_DIR"
fi

# Activate and install
source "$VENV_DIR/bin/activate"
pip install --upgrade pip

# Create requirements.txt
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

pip install -r requirements.txt

echo "✅ All packages installed in virtual environment."
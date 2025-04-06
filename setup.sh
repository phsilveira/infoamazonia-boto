#!/bin/bash
set -e

echo "Installing project dependencies..."
pip install --upgrade pip
pip install -e .
pip install -r requirements.txt

echo "Setup complete! You can now run the application with:"
echo "docker-compose up -d"

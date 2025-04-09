#!/bin/bash
set -e

# Install and update pip, wheel, and uv
python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install --upgrade uv

# Install the local package in development mode
python3 -m pip install -e src

# Seed the database
python3 src/fastapi_app/seed_data.py

# Start the application with gunicorn
python3 -m gunicorn fastapi_app:app -c src/gunicorn.conf.py
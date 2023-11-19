#!/bin/bash

echo "Creating 'output' directory..."
mkdir -p output

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies from requirements.txt..."
pip3 install -r ADITI_BHALAWAT_scraping_assignment/requirements.txt

echo "Running main.py..."
python3 ADITI_BHALAWAT_scraping_assignment/main.py

echo "Deactivating virtual environment..."
deactivate

echo "Setup complete!"

#!/bin/bash
cd "$(dirname "$0")"  # Go to the script's directory

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
# activate venv
source venv/bin/activate
# install dependencies, only needed once
# pip install -r requirements.txt > /dev/null 2>&1 
python3 main.py
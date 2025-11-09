#!/bin/bash

echo "========================================"
echo "  Dubai Smart Invest - Starting Server"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "========================================"
echo "  Starting Flask Server..."
echo "========================================"
echo ""
echo "Server will be available at:"
echo "  - Local:   http://localhost:5000"
echo "  - Network: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Press CTRL+C to stop the server"
echo "========================================"
echo ""

# Start the Flask application
python3 app.py

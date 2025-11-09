#!/bin/bash

# Le Blanc Dubai Real Estate - Setup Script
# This script sets up the backend and dependencies

echo "Setting up Le Blanc Dubai Real Estate Backend..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed. Please install pip."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For Unix/Linux/Mac
# For Windows: venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your actual email configuration."
fi

# Create leads file if it doesn't exist
if [ ! -f leads.json ]; then
    echo "Creating leads.json file..."
    echo "[]" > leads.json
fi

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your email configuration"
echo "2. Run 'python app.py' to start the server"
echo "3. Visit http://localhost:5000 to view the website"
echo ""
echo "For Windows users:"
echo "1. Use 'venv\\Scripts\\activate' to activate virtual environment"
echo "2. Make sure to configure your email settings in .env"
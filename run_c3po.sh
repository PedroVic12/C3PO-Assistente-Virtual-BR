#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install PM2 if not already installed
if ! command -v pm2 &> /dev/null; then
    echo "Installing PM2..."
    npm install -g pm2
fi

# Install dependencies if not already installed
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node.js dependencies..."
cd frontend
npm install
npm run build
cd ..

# Create static directory if it doesn't exist
mkdir -p static

# Start Flask backend with PM2
echo "Starting Flask backend..."
pm2 start "python serverView.py" --name "c3po-backend"

# Start React development server with PM2
echo "Starting React frontend..."
cd frontend
pm2 start "npm run dev" --name "c3po-frontend"

# Display PM2 processes
pm2 list

echo "C-3PO is now running!"
echo "Backend: http://localhost:9999"
echo "Frontend: http://localhost:8888"

#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored status messages
print_status() {
    echo -e "${YELLOW}[*] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[+] $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_status "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_success "Docker installed successfully!"
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_status "Docker Compose not found. Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed successfully!"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created!"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed successfully!"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    echo "MONGODB_URI=mongodb://localhost:27017" > .env
    echo "MONGODB_DB=voice_control_app" >> .env
    echo "GOOGLE_API_KEY=your_gemini_api_key" >> .env
    echo "STORAGE_PATH=$(pwd)/storage" >> .env
    print_success ".env file created! Please update with your actual API keys."
fi

# Create storage directory if it doesn't exist
if [ ! -d "storage" ]; then
    print_status "Creating storage directory..."
    mkdir storage
    print_success "Storage directory created!"
fi

# Build and start Docker containers
print_status "Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 5

print_success "Application is ready!"
print_success "Access the application at:"
echo "- Flask API: http://localhost:5000"
echo "- Flet UI: http://localhost:8550"

# Function to cleanup on script exit
cleanup() {
    print_status "Cleaning up..."
    docker-compose down
    deactivate
    print_success "Cleanup complete!"
}

# Register cleanup function
trap cleanup EXIT

# Keep the script running and show logs
print_status "Showing application logs (Ctrl+C to exit)..."
docker-compose logs -f

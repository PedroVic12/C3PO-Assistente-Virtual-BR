#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${YELLOW}[*] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[+] $1${NC}"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    echo "ANTHROPIC_API_KEY=your_anthropic_api_key" > .env
    echo "GOOGLE_SEARCH_API_KEY=your_google_search_api_key" >> .env
    echo "GOOGLE_SEARCH_CX=your_google_search_cx" >> .env
    print_success ".env file created! Please update with your actual API keys."
    exit 1
fi

# Build Docker image
print_status "Building Docker image..."
docker build -t blog-generator .

# Run Docker container
print_status "Starting Docker container..."
docker run -d \
    --name blog-generator \
    -p 5000:5000 \
    --env-file .env \
    blog-generator

print_success "Application is running!"
print_success "Access the application at: http://localhost:5000"

# Show logs
print_status "Showing application logs (Ctrl+C to exit)..."
docker logs -f blog-generator

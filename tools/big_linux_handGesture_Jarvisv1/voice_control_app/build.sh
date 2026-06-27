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

# Create and activate virtual environment
print_status "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Create executable with PyInstaller
print_status "Creating executable..."
pyinstaller blog_generator.spec

print_success "Build complete! Executable is in the dist directory."
print_success "To run the application:"
echo "1. cd dist"
echo "2. ./blog_generator"

# Cleanup
deactivate

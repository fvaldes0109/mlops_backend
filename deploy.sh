#!/bin/bash
set -e  # Exit on error

# Navigate to the deployment directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements if they exist
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Install gunicorn if not present
if ! command -v gunicorn &> /dev/null; then
    pip install gunicorn
fi

# Kill any existing server running on port 4742
echo "Stopping any existing server on port 4742..."
pkill -f "gunicorn.*:4742" || true

# Start the server in the background
echo "Starting server..."
nohup gunicorn -b :4742 --timeout 120 -w 4 main:app > server.log 2>&1 &

echo "Deployment completed successfully!"

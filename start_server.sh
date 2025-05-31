#!/bin/bash

echo "🔍 Checking for existing Flask processes..."

# Kill any existing Flask processes on port 5001
echo "🧹 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || echo "No processes found on port 5001"

# Also kill any python run.py processes
pkill -f "python run.py" 2>/dev/null || echo "No run.py processes found"

echo "✅ Cleanup complete!"

# Wait a moment for processes to fully terminate
sleep 2

echo "🚀 Starting Flask server..."
python run.py 
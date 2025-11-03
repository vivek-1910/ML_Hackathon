#!/bin/bash

# Hangman Web App Startup Script
# This script starts both the Flask backend and React frontend

echo "🎮 Starting Hangman Web Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "hangman-web/node_modules" ]; then
    echo "📦 Installing React dependencies..."
    cd hangman-web
    npm install
    cd ..
    echo "✓ React dependencies installed"
    echo ""
fi

# Start Flask backend in background
echo "🚀 Starting Flask backend on http://localhost:5001..."
python3 app.py &
FLASK_PID=$!
echo "✓ Flask backend started (PID: $FLASK_PID)"
echo ""

# Wait for Flask to initialize
sleep 3

# Start React frontend
echo "🚀 Starting React frontend on http://localhost:3000..."
cd hangman-web
npm start &
REACT_PID=$!
cd ..
echo "✓ React frontend started (PID: $REACT_PID)"
echo ""

echo "✅ Both servers are running!"
echo ""
echo "📝 Access the game at: http://localhost:3000"
echo "📝 Backend API at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $FLASK_PID $REACT_PID 2>/dev/null; echo '✓ Servers stopped'; exit 0" INT

# Keep script running
wait

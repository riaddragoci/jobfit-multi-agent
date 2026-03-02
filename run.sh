#!/bin/bash
# Run the CV ↔ JD Matcher Web Application
# Prerequisites: Python 3.10+, Node.js 18+, Ollama with llama3.1:8b

echo "⚡ CV ↔ JD Matcher — Starting Web Application"
echo "=============================================="
echo ""

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Install from: https://ollama.com"
    exit 1
fi

echo "✅ Ollama found"

# Check if llama3.1:8b model is available
if ! ollama list | grep -q "llama3.1:8b"; then
    echo "⬇️  Pulling llama3.1:8b model (this may take a while)..."
    ollama pull llama3.1:8b
fi

echo "✅ llama3.1:8b model ready"

# Install backend dependencies
echo ""
echo "📦 Installing backend dependencies..."
pip install -r backend/requirements.txt --quiet

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install --silent
cd ..

echo ""
echo "🚀 Starting backend (FastAPI) on http://localhost:8000"
echo "🚀 Starting frontend (Vite)   on http://localhost:5173"
echo ""
echo "   Open http://localhost:5173 in your browser!"
echo "   API docs at http://localhost:8000/docs"
echo ""

# Start backend in background
cd "$(dirname "$0")"
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!

# Trap exit to kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

# Wait for both
wait
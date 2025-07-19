#!/bin/bash
# Start the blog server and open it in browser

echo "🏴‍☠️ Starting blog server..."

# Kill any existing servers
pkill -f "python.*http.server" 2>/dev/null || true

# Start server in background
cd docs && python3 -m http.server 8000 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 1

# Open in default browser
echo "⚓ Opening blog in browser..."
open http://localhost:8000

echo "✨ Blog is running at http://localhost:8000"
echo "Press Ctrl+C to stop the server"

# Wait for user to stop
trap "kill $SERVER_PID 2>/dev/null; echo ''; echo '⚓ Server stopped!'; exit" INT
wait $SERVER_PID
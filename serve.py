#!/usr/bin/env python3
"""Simple local server for testing the blog."""

import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = "docs"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add cache control for development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def serve():
    """Start a local server."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🏴‍☠️ ARR! Blog server sailing at:")
        print(f"   http://localhost:{PORT}")
        print(f"   http://127.0.0.1:{PORT}")
        print(f"\nPress Ctrl+C to drop anchor and stop.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⚓ Server stopped. Fair winds!")
            sys.exit(0)

if __name__ == "__main__":
    serve()
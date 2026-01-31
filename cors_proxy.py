#!/usr/bin/env python3
"""
CORS Proxy для обхода CORS ограничений
Фронтенд → CORS Proxy (8001) → Backend (9000)
"""

import http.server
import socketserver
import json
from urllib.parse import urlparse
import urllib.request

PORT = 8001

class CORSProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests through proxy"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        # Все запросы идут на localhost:9000
        backend_url = f'http://localhost:9000{self.path}'
        
        try:
            req = urllib.request.Request(
                backend_url,
                data=body,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                result = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(result)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error = json.dumps({'status': 'error', 'message': str(e)})
            self.wfile.write(error.encode())
    
    def do_GET(self):
        """Handle GET requests through proxy"""
        backend_url = f'http://localhost:9000{self.path}'
        
        try:
            with urllib.request.urlopen(backend_url, timeout=5) as response:
                result = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error = json.dumps({'status': 'error', 'message': str(e)})
            self.wfile.write(error.encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[PROXY] {format % args}")

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CORSProxyHandler) as httpd:
        print(f"""
======================================================================
🌐 CORS PROXY SERVER
======================================================================
📍 Прокси на http://localhost:8001
🔗 Переадресовывает на http://localhost:9000
⏸️  Press Ctrl+C to stop
======================================================================
""")
        httpd.serve_forever()

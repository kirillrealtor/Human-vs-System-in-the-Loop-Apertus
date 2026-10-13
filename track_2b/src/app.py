"""
Entrypoint application for Hack Apertus Track 2B:
Serves the Interactive Dual-View Benchmark Dashboard & Inspection Suite.
"""

import os
import sys
import http.server
import socketserver

PORT = int(os.environ.get("PORT", 8080))

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        return super().do_GET()

def run_server():
    print("=" * 70)
    print("🏛️  Apertus Decision Support Suite — Hack Apertus Track 2B")
    print(f"🚀  Interactive Benchmark Dashboard running on port {PORT}")
    print(f"👉  Access URL: http://localhost:{PORT}")
    print("=" * 70)
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down dashboard server...")
            httpd.server_close()

if __name__ == "__main__":
    run_server()

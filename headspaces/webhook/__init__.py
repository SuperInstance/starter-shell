"""Webhook headspace — receive HTTP requests, file as PLATO tiles."""
import json, os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("WEBHOOK_PORT", "8080"))
SERVER = None

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        try:
            data = json.loads(body)
            from plato import PlatoClient
            client = PlatoClient()
            client.submit_tile("webhooks", 
                data.get("question", f"Webhook from {self.headers.get('User-Agent','unknown')}"),
                data.get("answer", body[:500]))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"tiled"}')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'{{"error":"{e}"}}'.encode())
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"listening","port":' + str(PORT).encode() + b'}')

def start():
    global SERVER
    SERVER = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    import threading
    t = threading.Thread(target=SERVER.serve_forever, daemon=True)
    t.start()
    return {"status": "running", "port": PORT}

def stop():
    global SERVER
    if SERVER: SERVER.shutdown()
    return {"status": "stopped"}

def status():
    return {"running": SERVER is not None}

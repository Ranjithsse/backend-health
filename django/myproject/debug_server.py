from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class DebugHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._log_request()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_POST(self):
        self._log_request()
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        print(f"Body: {body}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

    def _log_request(self):
        print(f"\n--- Incoming {self.command} request ---")
        print(f"Path: {self.path}")
        print(f"Headers:\n{self.headers}")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8000), DebugHandler)
    print("Starting debug server on 0.0.0.0:8000...")
    server.serve_forever()

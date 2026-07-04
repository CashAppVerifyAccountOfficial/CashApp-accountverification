from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from pathlib import Path
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / 'private-data'
DATA_FILE = DATA_DIR / 'submissions.jsonl'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write((ROOT / 'index.html').read_bytes())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != '/submit':
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        data = parse_qs(body)

        username = data.get('username', [''])[0].strip()
        password = data.get('password', [''])[0]

        if not username or not password:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Username and password are required.')
            return

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        record = {
            'username': username,
            'password': hashed_password,
            'submittedAt': __import__('datetime').datetime.utcnow().isoformat() + 'Z'
        }
        with DATA_FILE.open('a', encoding='utf-8') as f:
            f.write(json.dumps(record) + '\n')

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Saved securely.')

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), Handler)
    print('Server running at http://127.0.0.1:8000')
    server.serve_forever()

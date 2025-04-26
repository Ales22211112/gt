# Run this in a terminal with: python3 server.py
import http.server
import socketserver
import json
import requests

PORT = 8000
API_KEY = "YOUR_API_KEY_HERE"  # Replace this with your OpenAI API key

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user_input = json.loads(post_data.decode('utf-8'))

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": user_input['message']}
                ]
            }

            response = requests.post("https://api.openai.com/v1/chat/completions",
                                     headers=headers, json=data)
            self.send_response(response.status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response.content)
        else:
            self.send_error(404)

Handler = ProxyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
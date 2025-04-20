from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

# Store messages in memory
messages = []

class SimpleChatHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/":
            # Serve the HTML chat page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("chat.html", "r") as file:
                self.wfile.write(file.read().encode())
        
        elif self.path == "/messages":
            # Return the chat messages as JSON
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode())
        
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/":
            # Read POST data (username and message)
            length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(post_data)

            user = data.get("user", [""])[0]
            message = data.get("message", [""])[0]

            if user and message:
                # Store the message
                messages.append({"user": user, "message": message})

            # Redirect back to the chat page after posting the message
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

# Set up and run the server
def run():
    print("Server running on http://localhost:8000")
    server = HTTPServer(('localhost', 8000), SimpleChatHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()

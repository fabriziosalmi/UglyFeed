import http.server
import socket
import os
from urllib.parse import urljoin

# Define the directory and file to be served
uglyfeeds_dir = 'uglyfeeds'
uglyfeed_file = 'uglyfeed.xml'

# Change to the directory containing the uglyfeed.xml file
os.chdir(uglyfeeds_dir)

# Define a custom handler to serve the uglyfeed.xml file
class UglyFeedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = f'/{uglyfeed_file}'
        return super().do_GET()

# Function to get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

# Set up and start the server
def run(server_class=http.server.HTTPServer, handler_class=UglyFeedHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    local_ip = get_local_ip()
    final_url = urljoin(f'http://{local_ip}:{port}/', uglyfeed_file)
    print(f'Serving {uglyfeed_file} at: {final_url}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

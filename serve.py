import http.server
import socket
import os
from urllib.parse import urljoin

# Define the directory and file to be served
UGLYFEEDS_DIR = 'uglyfeeds'
UGLYFEED_FILE = 'uglyfeed.xml'

# Change to the directory containing the uglyfeed.xml file
os.chdir(UGLYFEEDS_DIR)


class UglyFeedHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve the uglyfeed.xml file."""
    def do_GET(self):
        if self.path == '/':
            self.path = f'/{UGLYFEED_FILE}'
        return super().do_GET()


def get_local_ip():
    """Get the local IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip


def run(server_class=http.server.HTTPServer, handler_class=UglyFeedHandler, port=8000):
    """Set up and start the server."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    local_ip = get_local_ip()
    final_url = urljoin(f'http://{local_ip}:{port}/', UGLYFEED_FILE)
    print(f'Serving {UGLYFEED_FILE} at: {final_url}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()

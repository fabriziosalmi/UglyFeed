import http.server
import socket
import os
import logging
import argparse
import signal
from urllib.parse import urljoin
from pathlib import Path
from configparser import ConfigParser
import psutil

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PID_FILE = 'uglyfeed_server.pid'

class UglyFeedHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve the specified file."""
    def __init__(self, *args, **kwargs):
        self.uglyfeed_file = kwargs.pop('uglyfeed_file')
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = f'/{self.uglyfeed_file}'
        # Security check to prevent directory traversal attacks
        if '..' in self.path or self.path.startswith(('/', '\\')):
            self.send_error(400, "Bad request")
            return
        return super().do_GET()

def get_local_ip():
    """Get the local IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            local_ip = s.getsockname()[0]
        except OSError:
            local_ip = '127.0.0.1'
    return local_ip

def run_server(directory, file_name, port):
    """Set up and start the server."""
    os.chdir(directory)

    def handler(*args, **kwargs):
        UglyFeedHandler(*args, uglyfeed_file=file_name, **kwargs)
    
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, handler)
    local_ip = get_local_ip()
    final_url = urljoin(f'http://{local_ip}:{port}/', file_name)
    logger.info(f'Serving {file_name} at: {final_url}')
    
    def graceful_shutdown(signum, frame):
        logger.info("Received signal to shut down the server")
        httpd.server_close()
        logger.info("Server shut down gracefully")
        if Path(PID_FILE).is_file():
            Path(PID_FILE).unlink()
    
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    # Write the PID file
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    try:
        httpd.serve_forever()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        httpd.server_close()
        if Path(PID_FILE).is_file():
            Path(PID_FILE).unlink()

def load_config(config_file):
    """Load configuration from a file."""
    default_dir = 'uglyfeeds'
    default_file = 'uglyfeed.xml'
    
    config = ConfigParser()
    if Path(config_file).is_file():
        config.read(config_file)
        directory = config.get('DEFAULT', 'UGLYFEEDS_DIR', fallback=default_dir)
        file_name = config.get('DEFAULT', 'UGLYFEED_FILE', fallback=default_file)
    else:
        directory = default_dir
        file_name = default_file

    return directory, file_name

def kill_existing_server():
    """Kill the existing server if it is already running."""
    if Path(PID_FILE).is_file():
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait()
                logger.info(f"Terminated existing server with PID: {pid}")
        except Exception as e:
            logger.error(f"Failed to terminate existing server: {e}")
        finally:
            Path(PID_FILE).unlink()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Serve an uglyfeed XML file.")
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port to serve on (default: 8000)')
    parser.add_argument('-c', '--config', type=str, default='config.ini', help='Configuration file (default: config.ini)')
    args = parser.parse_args()

    UGLYFEEDS_DIR, UGLYFEED_FILE = load_config(args.config)

    # Ensure the directory and file exist
    if not Path(UGLYFEEDS_DIR).is_dir():
        logger.error(f"The directory '{UGLYFEEDS_DIR}' does not exist.")
        exit(1)
    if not Path(UGLYFEEDS_DIR, UGLYFEED_FILE).is_file():
        logger.error(f"The file '{UGLYFEED_FILE}' does not exist in the directory '{UGLYFEEDS_DIR}'.")
        exit(1)

    # Kill any existing server
    kill_existing_server()

    run_server(UGLYFEEDS_DIR, UGLYFEED_FILE, args.port)

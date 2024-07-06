"""
This script starts an HTTP server to serve XML files with the correct content type and cache headers.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import shutil
from pathlib import Path
import os
from logging_setup import setup_logging, get_logger

# Initialize logging
logger = setup_logging()
server_logger = get_logger('server')

# Define directory paths and filenames
UGLYFEED_FILE = "uglyfeed.xml"  # Define this at the top with other constants
uglyfeed_file = UGLYFEED_FILE  # Alias for UGLYFEED_FILE
UGLYFEEDS_DIR = Path("uglyfeeds")
STATIC_DIR = Path(".streamlit") / "static" / "uglyfeeds"

class CustomXMLHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler to serve XML files with correct content type and cache headers."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path.endswith(".xml"):
            self._serve_xml_file()
        else:
            super().do_GET()

    def _serve_xml_file(self):
        """Serve an XML file with appropriate headers."""
        file_path = STATIC_DIR / self.path.lstrip('/')

        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0")
            self.end_headers()

            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
            server_logger.info("Served XML file: %s", file_path)
        else:
            self.send_error(404, "File not found")
            server_logger.warning("XML file not found: %s", file_path)

def start_http_server(port):
    """Start the HTTP server to serve XML files."""
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, CustomXMLHandler)
        server_logger.info("Starting server on port %d", port)
        httpd.serve_forever()
    except Exception as e:
        server_logger.error("Failed to start server on port %d: %s", port, e)
        raise

def toggle_server(start, port, session_state):
    """Toggle the HTTP server on or off."""
    if start:
        if not session_state.get('server_thread') or not session_state['server_thread'].is_alive():
            session_state['server_thread'] = threading.Thread(target=start_http_server, args=(port,), daemon=True)
            session_state['server_thread'].start()
            server_logger.info("Server started on port %d.", port)
        else:
            server_logger.info("Server is already running.")
    else:
        if session_state.get('server_thread') and session_state['server_thread'].is_alive():
            session_state['server_thread'] = None
            server_logger.info("Server stopped.")
        else:
            server_logger.info("Server is not running.")

def copy_xml_to_static():
    """Copy the XML file to the Streamlit static directory if it exists."""
    source_file = UGLYFEEDS_DIR / UGLYFEED_FILE
    destination_file = STATIC_DIR / UGLYFEED_FILE

    if source_file.exists() and source_file.is_file():
        os.makedirs(STATIC_DIR, exist_ok=True)
        shutil.copy(source_file, destination_file)
        server_logger.info("Copied %s to %s.", UGLYFEED_FILE, STATIC_DIR)
        return destination_file
    else:
        server_logger.warning("Source file %s does not exist in %s.", UGLYFEED_FILE, UGLYFEEDS_DIR)
        return None

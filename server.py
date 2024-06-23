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
static_dir = Path(".streamlit") / "static" / "uglyfeeds"
uglyfeeds_dir = Path("uglyfeeds")
uglyfeed_file = "uglyfeed.xml"  # Retain the original variable name for compatibility

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
        file_path = static_dir / self.path.lstrip('/')

        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0")
            self.end_headers()

            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
            server_logger.info(f"Served XML file: {file_path}")
        else:
            self.send_error(404, "File not found")
            server_logger.warning(f"XML file not found: {file_path}")

def start_http_server(port):
    """Start the HTTP server to serve XML files."""
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, CustomXMLHandler)
        server_logger.info(f"Starting server on port {port}")
        httpd.serve_forever()
    except Exception as e:
        server_logger.error(f"Failed to start server on port {port}: {e}")
        raise

def toggle_server(start, port, session_state):
    """Toggle the HTTP server on or off."""
    if start:
        if not session_state.get('server_thread') or not session_state['server_thread'].is_alive():
            session_state['server_thread'] = threading.Thread(target=start_http_server, args=(port,), daemon=True)
            session_state['server_thread'].start()
            server_logger.info(f"Server started on port {port}.")
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
    source_file = uglyfeeds_dir / uglyfeed_file
    destination_file = static_dir / uglyfeed_file

    if source_file.exists() and source_file.is_file():
        os.makedirs(static_dir, exist_ok=True)
        shutil.copy(source_file, destination_file)
        server_logger.info(f"Copied {uglyfeed_file} to {static_dir}.")
        return destination_file
    else:
        server_logger.warning(f"Source file {uglyfeed_file} does not exist in {uglyfeeds_dir}.")
        return None

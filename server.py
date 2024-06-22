from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import shutil
from pathlib import Path
import os

static_dir = Path(".streamlit") / "static" / "uglyfeeds"
uglyfeeds_dir = Path("uglyfeeds")
uglyfeed_file = "uglyfeed.xml"

class XMLHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler to serve XML with correct content type and cache headers."""
    def do_GET(self):
        if self.path.endswith(".xml"):
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0")
            self.end_headers()
            with open(static_dir / self.path.lstrip('/'), 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

def start_custom_server(port):
    """Start the HTTP server to serve XML."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, XMLHTTPRequestHandler)
    httpd.serve_forever()

def toggle_server(start, port, session_state):
    """Toggle the HTTP server on or off."""
    if start:
        if session_state.server_thread is None or not session_state.server_thread.is_alive():
            session_state.server_thread = threading.Thread(target=start_custom_server, args=(port,), daemon=True)
            session_state.server_thread.start()
    else:
        if session_state.server_thread and session_state.server_thread.is_alive():
            session_state.server_thread = None

def copy_xml_to_static():
    """Ensure XML is copied to Streamlit static directory."""
    if uglyfeeds_dir.exists() and (uglyfeeds_dir / uglyfeed_file).exists():
        destination_path = static_dir / uglyfeed_file
        shutil.copy(uglyfeeds_dir / uglyfeed_file, destination_path)
        return destination_path
    return None

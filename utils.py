"""
This script provides utility functions for handling socket operations and XML file statistics.
"""

import socket
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

# Define directory paths and filenames
UGLYFEEDS_DIR = Path("uglyfeeds")
UGLYFEED_FILE = "uglyfeed.xml"

def get_local_ip():
    """Get the local IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('10.254.254.254', 1))
            local_ip = s.getsockname()[0]
        except OSError:
            local_ip = '127.0.0.1'
    return local_ip

def find_available_port(base_port):
    """Find an available port starting from a base port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                s.bind(("", base_port))
                s.close()
                return base_port
            except OSError:
                base_port += 1

def get_xml_item_count():
    """Get the current count of items in the XML."""
    if not (UGLYFEEDS_DIR / UGLYFEED_FILE).exists():
        return 0
    tree = ET.parse(UGLYFEEDS_DIR / UGLYFEED_FILE)
    root = tree.getroot()
    items = root.findall(".//item")
    return len(items)

def get_new_item_count(old_count):
    """Calculate the new items count based on the old count."""
    new_count = get_xml_item_count()
    if old_count is None or new_count is None:
        return 0
    return new_count - old_count

def get_xml_stats():
    """Get quick stats from the XML file."""
    if not (UGLYFEEDS_DIR / UGLYFEED_FILE).exists():
        return None, None, None
    tree = ET.parse(UGLYFEEDS_DIR / UGLYFEED_FILE)
    root = tree.getroot()
    items = root.findall(".//item")
    item_count = len(items)
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item_count, last_updated, UGLYFEEDS_DIR / UGLYFEED_FILE

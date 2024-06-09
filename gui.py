import streamlit as st
import os
import subprocess
import yaml
import json
from pathlib import Path
import socket
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Define paths for the feeds.txt and config.yaml files
feeds_path = Path("input/feeds.txt")
config_path = Path("config.yaml")
uglyfeeds_dir = Path("uglyfeeds")
uglyfeed_file = "uglyfeed.xml"
static_dir = Path(".streamlit") / "static" / "uglyfeeds"

# Ensure necessary directories and files exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("rewritten", exist_ok=True)
os.makedirs(uglyfeeds_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

# Default RSS feed URLs
default_feeds = """https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml
https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-2.xml
https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-3.xml"""

# Clone the repository automatically if it does not exist
repo_url = "https://github.com/fabriziosalmi/UglyFeed"
repo_path = Path("UglyFeed")

def clone_repo():
    if not repo_path.exists():
        with st.spinner("Cloning the UglyFeed repository..."):
            subprocess.run(["git", "clone", repo_url], check=True)
            st.success("Repository cloned into UglyFeed folder")

clone_repo()

# Load existing configuration if available
def load_config():
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    else:
        return None

# Save configuration and feeds
def save_configuration():
    with open(config_path, "w") as f:
        yaml.dump(st.session_state.config_data, f)
    with open(feeds_path, "w") as f:
        f.write(st.session_state.feeds)
    st.success("Configuration and feeds saved")

# Initialize session state for config data
if 'config_data' not in st.session_state:
    st.session_state.config_data = load_config() or {
        'similarity_threshold': 0.66,
        'similarity_options': {
            'min_samples': 2,
            'eps': 0.66
        },
        'api_config': {
            'ollama_api_url': "http://localhost:11434/api/chat",
            'ollama_model': "phi3"
        },
        'folders': {
            'output_folder': "output",
            'rewritten_folder': "rewritten"
        },
        'content_prefix': "In qualità di giornalista esperto, utilizza un tono professionale, preciso e dettagliato...",
        'max_items': 50,
        'max_age_days': 10
    }

# Function to get the local IP address
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

# Function to run scripts and display output
def run_script(script_name):
    """Execute a script and display its output in Streamlit."""
    with st.spinner(f"Executing {script_name}..."):
        process = subprocess.run(["python", script_name], capture_output=True, text=True)
        st.text_area(f"Output of {script_name}", process.stdout or "No output", height=200)
        if process.stderr:
            st.text_area(f"Errors or logs of {script_name}", process.stderr, height=200)

# Custom HTTP handler to serve XML with correct content type
class XMLHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(".xml"):
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.end_headers()
            with open(static_dir / self.path.lstrip('/'), 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

def start_custom_server():
    server_address = ('', 8001)  # Using a different port to avoid conflicts with Streamlit
    httpd = HTTPServer(server_address, XMLHTTPRequestHandler)
    httpd.serve_forever()

# Start the custom server in a new thread
server_thread = threading.Thread(target=start_custom_server, daemon=True)
server_thread.start()

# Sidebar navigation
st.sidebar.title("Navigation")
menu_options = ["Configuration", "Run main.py", "Run llm_processor.py", "Run json2rss.py", "View and Serve XML", "JSON Viewer"]
selected_option = st.sidebar.selectbox("Select an option", menu_options)

# Configuration Section
if selected_option == "Configuration":
    st.header("Configuration")

    st.subheader("RSS Feeds")
    if not feeds_path.exists():
        st.session_state.feeds = default_feeds
    else:
        with open(feeds_path, "r") as f:
            st.session_state.feeds = f.read()

    st.session_state.feeds = st.text_area("Enter one RSS feed URL per line:", st.session_state.feeds)

    if st.button("Save Feeds to input/feeds.txt"):
        with open(feeds_path, "w") as f:
            f.write(st.session_state.feeds)
        st.success("Feeds saved to input/feeds.txt")

    st.divider()

    st.subheader("Similarity Options")
    st.session_state.config_data['similarity_threshold'] = st.slider("Similarity Threshold", 0.0, 1.0, st.session_state.config_data['similarity_threshold'])
    st.session_state.config_data['similarity_options']['min_samples'] = st.number_input("Minimum Samples", min_value=1, value=st.session_state.config_data['similarity_options']['min_samples'])
    st.session_state.config_data['similarity_options']['eps'] = st.number_input("Epsilon (eps)", min_value=0.0, value=st.session_state.config_data['similarity_options']['eps'], step=0.01)

    st.subheader("API and LLM Options")
    api_options = ["OpenAI", "Groq", "Ollama"]
    selected_api = st.selectbox("Select API", api_options)
    if selected_api == "OpenAI":
        st.session_state.config_data['api_config'] = {
            'openai_api_url': st.text_input("OpenAI API URL", "https://api.openai.com/v1/chat/completions"),
            'openai_api_key': st.text_input("OpenAI API Key", type="password"),
            'openai_model': st.text_input("OpenAI Model", "gpt-3.5-turbo")
        }
    elif selected_api == "Groq":
        st.session_state.config_data['api_config'] = {
            'groq_api_url': st.text_input("Groq API URL", "https://api.groq.com/openai/v1/chat/completions"),
            'groq_api_key': st.text_input("Groq API Key", type="password"),
            'groq_model': st.text_input("Groq Model", "llama3-70b-8192")
        }
    else:
        st.session_state.config_data['api_config'] = {
            'ollama_api_url': st.text_input("Ollama API URL", "http://localhost:11434/api/chat"),
            'ollama_model': st.text_input("Ollama Model", "phi3")
        }

    st.subheader("Content Prefix")
    st.session_state.config_data['content_prefix'] = st.text_area("Content Prefix", st.session_state.config_data['content_prefix'])

    st.subheader("RSS Retention Options")
    st.session_state.config_data['max_items'] = st.number_input("Maximum Items", min_value=1, value=st.session_state.config_data['max_items'])
    st.session_state.config_data['max_age_days'] = st.number_input("Maximum Age (days)", min_value=1, value=st.session_state.config_data['max_age_days'])

    st.divider()
    if st.button("Load Configuration"):
        st.session_state.config_data = load_config() or st.session_state.config_data
        st.experimental_rerun()

    if st.button("Reset to Default"):
        st.session_state.config_data = {
            'similarity_threshold': 0.66,
            'similarity_options': {
                'min_samples': 2,
                'eps': 0.66
            },
            'api_config': {
                'ollama_api_url': "http://localhost:11434/api/chat",
                'ollama_model': "phi3"
            },
            'folders': {
                'output_folder': "output",
                'rewritten_folder': "rewritten"
            },
            'content_prefix': "In qualità di giornalista esperto, utilizza un tono professionale, preciso e dettagliato...",
            'max_items': 50,
            'max_age_days': 10
        }
        st.session_state.feeds = default_feeds
        st.experimental_rerun()

    st.divider()
    if st.button("Save Configuration and Feeds"):
        save_configuration()

# Run main.py Section
elif selected_option == "Run main.py":
    st.header("Run main.py")
    if st.button("Run main.py"):
        run_script("main.py")

# Run llm_processor.py Section
elif selected_option == "Run llm_processor.py":
    st.header("Run llm_processor.py")
    if st.button("Run llm_processor.py"):
        run_script("llm_processor.py")

# Run json2rss.py Section
elif selected_option == "Run json2rss.py":
    st.header("Run json2rss.py")
    if st.button("Run json2rss.py"):
        run_script("json2rss.py")

# View and Serve XML Section
elif selected_option == "View and Serve XML":
    st.header("View and Serve XML")

    # Ensure the file exists
    xml_file_path = uglyfeeds_dir / uglyfeed_file
    if not xml_file_path.exists():
        st.warning(f"The file '{uglyfeed_file}' does not exist in the directory '{uglyfeeds_dir}'.")
    else:
        # Copy the XML file to the Streamlit static directory
        destination_path = static_dir / uglyfeed_file
        shutil.copy(xml_file_path, destination_path)
        
        # Display the XML file content
        with open(xml_file_path, "r") as f:
            xml_content = f.read()
        st.text_area("XML Content", xml_content, height=300)

        # Provide a direct download link for the XML file
        with open(destination_path, "rb") as f:
            st.download_button(
                label="Download XML File",
                data=f,
                file_name=uglyfeed_file,
                mime="application/xml"
            )

        # Provide a link to serve the XML file
        local_ip = get_local_ip()
        custom_server_port = 8001  # Port for the custom server
        serve_url = f"http://{local_ip}:{custom_server_port}/{uglyfeed_file}"
        st.markdown(f"**Serve URL:** [Open XML File]({serve_url})")

        # Show the local IP and full link for easier access
        st.info(f"Serving `{uglyfeed_file}` at: {serve_url}")

# JSON Viewer Section
elif selected_option == "JSON Viewer":
    st.header("JSON Viewer")

    json_files = list(Path("rewritten").glob("*.json"))

    if json_files:
        selected_file = st.selectbox("Select a JSON file to view", json_files)

        if selected_file:
            with open(selected_file, "r") as f:
                json_data = json.load(f)

            st.json(json_data)

            json_str = json.dumps(json_data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=selected_file.name,
                mime="application/json"
            )
    else:
        st.info("No JSON files found in the rewritten folder")

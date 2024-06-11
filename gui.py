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
import schedule
import time
import xml.etree.ElementTree as ET
from datetime import datetime

# Define paths
feeds_path = Path("input/feeds.txt")
config_path = Path("config.yaml")
uglyfeeds_dir = Path("uglyfeeds")
uglyfeed_file = "uglyfeed.xml"
static_dir = Path(".streamlit") / "static" / "uglyfeeds"
version_file = Path("version.txt")
docs_dir = Path("docs")  # Path to the documentation directory

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

# Repository URL and path
repo_url = "https://github.com/fabriziosalmi/UglyFeed"
repo_path = Path("UglyFeed")

# Global variable to hold the last run output
last_run_output = []

def get_local_version():
    """Get the local version from version.txt."""
    if version_file.exists():
        with open(version_file, "r") as f:
            return f.read().strip()
    return None

def get_remote_version(repo_url):
    """Get the remote version by fetching version.txt from the remote repository."""
    try:
        remote_version_url = f"https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/version.txt"
        result = subprocess.run(["curl", "-s", remote_version_url], capture_output=True, text=True, check=True)
        if result.stdout:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred while fetching the remote version: {e}")
    return None

def check_and_update_repo(repo_path, repo_url):
    """Check if the remote repo has updates and pull them if available."""
    try:
        local_version = get_local_version()
        remote_version = get_remote_version(repo_url)
        if local_version and remote_version:
            if remote_version > local_version:
                st.write(f"Remote version ({remote_version}) is newer than local version ({local_version}). Updating repository...")
                if repo_path.exists():
                    os.chdir(repo_path)
                    with st.spinner("Pulling updates from the remote repository..."):
                        subprocess.run(["git", "pull"], check=True)
                        st.success(f"Repository updated to version {remote_version}.")
                else:
                    with st.spinner("Cloning the UglyFeed repository..."):
                        subprocess.run(["git", "clone", repo_url], check=True)
                        st.success(f"Repository cloned with version {remote_version}.")
            else:
                st.info(f"The local repository is already up-to-date. (version: {local_version})")
        else:
            st.error("Unable to determine versions for comparison.")
    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred while checking the repository: {e}")

# Load existing configuration if available
def load_config():
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    else:
        return None

# Ensure all required keys are in the config_data with default values
def ensure_default_config(config_data):
    """Ensure the configuration dictionary contains default values for missing keys."""
    defaults = {
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
        'max_age_days': 10,
        'scheduling_enabled': False,
        'scheduling_interval': 1,
        'scheduling_period': 'hours'
    }

    # Recursively update the config_data with any missing default keys
    def recursive_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = recursive_update(d.get(k, {}), v)
            else:
                d.setdefault(k, v)
        return d

    return recursive_update(config_data, defaults)

# Initialize session state for config data
if 'config_data' not in st.session_state:
    st.session_state.config_data = ensure_default_config(load_config() or {})

# Save configuration and feeds
def save_configuration(overwrite):
    """Save the current configuration to config.yaml and feeds.txt."""
    if overwrite:
        with open(config_path, "w") as f:
            yaml.dump(st.session_state.config_data, f)
        st.success("Configuration saved to config.yaml")
    else:
        st.info("Configuration changes not saved to avoid overwriting.")

# Function to get the local IP address
def get_local_ip():
    """Get the local IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('10.254.254.254', 1))
            local_ip = s.getsockname()[0]
        except OSError:
            local_ip = '127.0.0.1'
    return local_ip

# Function to find an available port starting from a base port
def find_available_port(base_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                s.bind(("", base_port))
                s.close()
                return base_port
            except OSError:
                base_port += 1

# Function to run a script and display its output
def run_script(script_name):
    """Execute a script and display its output in Streamlit."""
    with st.spinner(f"Executing {script_name}..."):
        process = subprocess.run(["python", script_name], capture_output=True, text=True)
        st.text_area(f"Output of {script_name}", process.stdout or "No output", height=200)
        if process.stderr:
            st.text_area(f"Errors or logs of {script_name}", process.stderr, height=200)

# Function to run scripts sequentially and display output
def run_scripts_sequentially():
    """Run main.py, llm_processor.py, and json2rss.py sequentially."""
    global last_run_output
    last_run_output = []
    scripts = ["main.py", "llm_processor.py", "json2rss.py"]
    for script in scripts:
        with st.spinner(f"Executing {script}..."):
            process = subprocess.run(["python", script], capture_output=True, text=True)
            output = process.stdout or "No output"
            errors = process.stderr or ""
            st.text_area(f"Output of {script}", output, height=200)
            if errors:
                st.text_area(f"Errors or logs of {script}", errors, height=200)
            last_run_output.append((script, output, errors))

# Custom HTTP handler to serve XML with correct content type
class XMLHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(".xml"):
            try:
                # Define the only allowed file to serve
                allowed_files = {"uglyfeed.xml"}
                
                # Sanitize and resolve the path
                requested_file = os.path.basename(self.path)
                
                if requested_file not in allowed_files:
                    self.send_error(403, "Forbidden: Access is denied.")
                    return
                
                file_path = static_dir / requested_file
                
                # Ensure the file exists within the static directory
                if file_path.exists() and file_path.is_file():
                    self.send_response(200)
                    self.send_header("Content-Type", "application/xml")
                    self.end_headers()
                    with open(file_path, 'rb') as file:
                        self.wfile.write(file.read())
                else:
                    self.send_error(404, "File not found")
            except Exception as e:
                self.send_error(500, f"Internal Server Error: {e}")
        else:
            super().do_GET()

def start_custom_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, XMLHTTPRequestHandler)
    httpd.serve_forever()

# Start the custom server in a new thread on an available port
custom_server_port = find_available_port(8001)
server_thread = threading.Thread(target=start_custom_server, args=(custom_server_port,), daemon=True)
server_thread.start()

# Ensure XML is copied to Streamlit static directory
def copy_xml_to_static():
    if uglyfeeds_dir.exists() and (uglyfeeds_dir / uglyfeed_file).exists():
        destination_path = static_dir / uglyfeed_file
        shutil.copy(uglyfeeds_dir / uglyfeed_file, destination_path)
        return destination_path
    return None

# Function to list all Markdown files in the docs directory
def list_markdown_files(docs_dir):
    return [file for file in docs_dir.glob("*.md")]

# Function to get quick stats from the XML file
def get_xml_stats():
    if not (uglyfeeds_dir / uglyfeed_file).exists():
        return None, None, None
    tree = ET.parse(uglyfeeds_dir / uglyfeed_file)
    root = tree.getroot()
    items = root.findall(".//item")
    item_count = len(items)
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item_count, last_updated, uglyfeeds_dir / uglyfeed_file

# Function to schedule jobs
def schedule_jobs(interval, period):
    def job():
        run_scripts_sequentially()

    if period == 'minutes':
        schedule.every(interval).minutes.do(job)
    elif period == 'hours':
        schedule.every(interval).hours.do(job)
    elif period == 'days':
        schedule.every(interval).days.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduling if enabled in the config
if st.session_state.config_data.get('scheduling_enabled', False):
    scheduling_thread = threading.Thread(target=schedule_jobs, args=(st.session_state.config_data['scheduling_interval'], st.session_state.config_data['scheduling_period']), daemon=True)
    scheduling_thread.start()

# Sidebar navigation
st.sidebar.title("Navigation")
menu_options = ["Introduction", "Configuration", "Run Scripts", "Run main.py", "Run llm_processor.py", "Run json2rss.py", "View and Serve XML", "Scheduled Jobs", "Documentation"]
selected_option = st.sidebar.selectbox("Select an option", menu_options)

# Introduction Page
if selected_option == "Introduction":
    st.title("UglyFeed")
    st.image("docs/UglyFeed.png", width=300, use_column_width='auto')
    st.write("""
        This application provides a graphical user interface to manage and process RSS feeds using the UglyFeed project.
        Use the sidebar to navigate through different functionalities of the application:

        - **Configuration**: Set up and save your RSS feeds and processing options.
        - **Run Scripts**: Execute various processing scripts like `main.py`, `llm_processor.py`, and `json2rss.py`.
        - **View and Serve XML**: View the content of the XML feed and serve it via a custom HTTP server.
        - **Scheduled Jobs**: Configure and view the output of scheduled jobs.
        - **Documentation**: View the Markdown documentation files related to the project.

        Make sure your local environment is configured correctly and that the necessary directories and files are in place. For any bug just [open an issue](https://github.com/fabriziosalmi/UglyFeed/issues/new/choose) on GitHub, hopefully I'll be able to fix it ^_^. Enjoy!
    """)

# Configuration Section
elif selected_option == "Configuration":
    st.header("Configuration")

    st.subheader("Version and Repository Management")
    check_and_update_repo(repo_path, repo_url)
    st.divider()

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

    st.divider()

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

    st.divider()

    st.subheader("Content Prefix")
    st.session_state.config_data['content_prefix'] = st.text_area("Content Prefix", st.session_state.config_data['content_prefix'])

    st.divider()

    st.subheader("RSS Retention Options")
    st.session_state.config_data['max_items'] = st.number_input("Maximum Items", min_value=1, value=st.session_state.config_data['max_items'])
    st.session_state.config_data['max_age_days'] = st.number_input("Maximum Age (days)", min_value=1, value=st.session_state.config_data['max_age_days'])

    st.divider()

    # Add a checkbox to control the overwriting of config.yaml
    overwrite_config = st.checkbox("Force overwrite config.yaml", value=False)

    if st.button("Save Configuration and Feeds"):
        save_configuration(overwrite_config)

# Run Scripts Section
elif selected_option == "Run Scripts":
    st.header("Run Scripts")

    if st.button("Run main.py, llm_processor.py, and json2rss.py sequentially"):
        run_scripts_sequentially()

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

    # Ensure the file exists and copy it to the static directory
    xml_file_path = copy_xml_to_static()
    if not xml_file_path:
        st.warning(f"The file '{uglyfeed_file}' does not exist in the directory '{uglyfeeds_dir}'.")
    else:
        # Display the XML file content
        with open(xml_file_path, "r") as f:
            xml_content = f.read()
        st.text_area("XML Content", xml_content, height=300)

        # Provide a direct download link for the XML file
        with open(xml_file_path, "rb") as f:
            st.download_button(
                label="Download XML File",
                data=f,
                file_name=uglyfeed_file,
                mime="application/xml"
            )

        # Provide a link to serve the XML file through the custom server
        local_ip = get_local_ip()
        serve_url = f"http://{local_ip}:{custom_server_port}/{uglyfeed_file}"

        # Display the serve URL in a clean format
        st.markdown(f"**Serving `{uglyfeed_file}` at:**\n\n[{serve_url}]({serve_url})")

# Scheduled Jobs Section
elif selected_option == "Scheduled Jobs":
    st.header("Scheduled Jobs")

    # Display the scheduling configuration and status
    st.subheader("Scheduling Configuration")
    scheduling_enabled = st.session_state.config_data.get('scheduling_enabled', False)

    # Predefined scheduling intervals
    interval_options = {
        "1 hour": (1, 'hours'),
        "4 hours": (4, 'hours'),
        "12 hours": (12, 'hours'),
        "24 hours": (24, 'hours')
    }

    # Default to "1 hour" if not set
    current_interval = st.session_state.config_data.get('scheduling_interval', 1)
    current_period = st.session_state.config_data.get('scheduling_period', 'hours')
    default_option = next((k for k, v in interval_options.items() if v == (current_interval, current_period)), "1 hour")

    st.session_state.config_data['scheduling_enabled'] = st.checkbox("Enable Scheduled Execution", value=scheduling_enabled)
    selected_interval = st.selectbox("Select Scheduling Interval", list(interval_options.keys()), index=list(interval_options.keys()).index(default_option))

    # Update session state based on selection
    interval, period = interval_options[selected_interval]
    st.session_state.config_data['scheduling_interval'] = interval
    st.session_state.config_data['scheduling_period'] = period

    # Save the scheduling configuration
    if st.button("Save Scheduling Configuration"):
        save_configuration(True)
        st.success("Scheduling configuration saved.")

    st.write(f"Scheduling Enabled: **{st.session_state.config_data['scheduling_enabled']}**")
    st.write(f"Selected Interval: **{selected_interval}**")

    # Show the last run output
    st.subheader("Last Run Output")
    if last_run_output:
        for script, output, errors in last_run_output:
            st.markdown(f"**Output of `{script}`:**")
            st.text_area(f"Output of {script}", output, height=200)
            if errors:
                st.text_area(f"Errors or logs of {script}", errors, height=200)
    else:
        st.info("No scheduled runs have occurred yet.")

    # Display quick stats for the XML file
    st.subheader("XML File Stats")
    item_count, last_updated, xml_path = get_xml_stats()
    if item_count is not None:
        st.write(f"**Item Count:** {item_count}")
        st.write(f"**Last Updated:** {last_updated}")
        st.write(f"**File Path:** {xml_path}")
    else:
        st.info("No XML file found or file is empty.")

# Documentation Section
elif selected_option == "Documentation":
    st.header("Documentation")

    # Display README.md by default
    readme_path = docs_dir / "README.md"
    if readme_path.exists():
        with open(readme_path, "r") as f:
            readme_content = f.read()
        st.markdown(readme_content)
    else:
        st.info("No README.md found in the docs folder.")

    st.subheader("Additional Documentation Files")
    markdown_files = list_markdown_files(docs_dir)
    if markdown_files:
        selected_file = st.selectbox("Select a documentation file to view", markdown_files)

        if selected_file:
            with open(selected_file, "r") as f:
                content = f.read()
            st.markdown(content)
    else:
        st.info("No additional documentation files found in the docs folder.")

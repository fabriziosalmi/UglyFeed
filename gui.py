import streamlit as st
import os
import requests
import psutil
import subprocess
import yaml
import socket
import shutil
import threading
import schedule
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

import logging
import streamlit as st

# Define a custom logging filter
class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level
    def filter(self, record):
        return record.levelno >= self.level

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a stream handler for capturing logs
info_handler = logging.StreamHandler()
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Create another stream handler for error logs
error_handler = logging.StreamHandler()
error_handler.setLevel(logging.WARNING)  # Capturing WARNING and above
error_handler.addFilter(LevelFilter(logging.WARNING))
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)




# Define paths
feeds_path = Path("input/feeds.txt")
config_path = Path("config.yaml")
uglyfeeds_dir = Path("uglyfeeds")
uglyfeed_file = "uglyfeed.xml"
static_dir = Path(".streamlit") / "static" / "uglyfeeds"
version_file = Path("version.txt")
docs_dir = Path("docs")

# Ensure necessary directories and files exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("rewritten", exist_ok=True)
os.makedirs(uglyfeeds_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

# Global variable to hold job execution stats
job_stats_global = []

def load_config():
    """Load existing configuration if available."""
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

def ensure_default_config(config_data):
    """Ensure all required keys are in the config_data with default values."""
    defaults = {
        'similarity_threshold': 0.66,
        'similarity_options': {
            'min_samples': 2,
            'eps': 0.66
        },
        'api_config': {
            'selected_api': "OpenAI",
            'openai_api_url': "https://api.openai.com/v1/chat/completions",
            'openai_api_key': "",
            'openai_model': "gpt-3.5-turbo",
            'groq_api_url': "https://api.groq.com/openai/v1/chat/completions",
            'groq_api_key': "",
            'groq_model': "llama3-70b-8192",
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
        'scheduling_interval': 2,
        'scheduling_period': 'minutes',
        'feed_title': "UglyFeed RSS",
        'feed_link': "https://github.com/fabriziosalmi/UglyFeed",
        'feed_description': "This is a default description for the feed.",
        'feed_language': "it",
        'feed_self_link': "https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml",
        'author': "UglyFeed",
        'category': "Fun",
        'copyright': "None",
        'http_server_port': 8001  # Default server port
    }

    def recursive_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = recursive_update(d.get(k, {}), v)
            else:
                d.setdefault(k, v)
        return d

    return recursive_update(config_data, defaults)




def save_configuration():
    """Save configuration and feeds to file."""
    with open(config_path, "w") as f:
        yaml.dump(st.session_state.config_data, f)
    with open(feeds_path, "w") as f:
        f.write(st.session_state.feeds)
    st.success("Configuration and feeds saved.")

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

def run_script(script_name):
    """Execute a script and capture its output and errors."""
    process = subprocess.run(["python", script_name], capture_output=True, text=True)
    output = process.stdout.strip() if process.stdout else "No output"
    errors = process.stderr.strip() if process.stderr else "No errors"
    return output, errors

def run_scripts_sequentially():
    """Run main.py, llm_processor.py, and json2rss.py sequentially and log their outputs."""
    global job_stats_global
    scripts = ["main.py", "llm_processor.py", "json2rss.py"]
    item_count_before = get_xml_item_count()

    # Prepare containers for output and error logs
    info_log_content = []
    error_log_content = []

    for script in scripts:
        with st.spinner(f"Executing {script}..."):
            output, errors = run_script(script)

            # Collect logs for Streamlit display
            info_log_content.append(f"Output of {script}:\n{output}")
            if errors.strip() and errors != "No errors":
                error_log_content.append(f"Errors or logs of {script}:\n{errors}")

            # Log output and errors
            logger.info(f"Output of {script}:\n{output}")
            if errors.strip() and errors != "No errors":
                logger.error(f"Errors or logs of {script}:\n{errors}")

            # Display real useful informations in Streamlit text areas
            st.text_area(f"Output of {script}", errors, height=200)

    new_items = get_new_item_count(item_count_before)
    job_stats_global.append({
        'script': ', '.join(scripts),
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'Success',
        'new_items': new_items
    })



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

def get_config_value(config, key, default_value):
    """Get the configuration value from environment variables, config file, or default."""
    return os.getenv(key.upper(), config.get(key, default_value))

def start_custom_server(port):
    """Start the HTTP server to serve XML."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, XMLHTTPRequestHandler)
    httpd.serve_forever()

def stop_server():
    """Stop the HTTP server."""
    if st.session_state.server_thread and st.session_state.server_thread.is_alive():
        # Set the server thread to None to signal it should stop
        st.session_state.server_thread = None
        st.warning("Server stopped. Please restart the application to stop the server completely.")
    else:
        st.info("Server is not running.")

def toggle_server(start):
    """Toggle the HTTP server on or off."""
    if start:
        if st.session_state.server_thread is None or not st.session_state.server_thread.is_alive():
            # Get the port from the session state, environment variable, or config file
            port = int(get_config_value(st.session_state.config_data, 'http_server_port', 8001))
            st.session_state.custom_server_port = port
            st.session_state.server_thread = threading.Thread(target=start_custom_server, args=(st.session_state.custom_server_port,), daemon=True)
            st.session_state.server_thread.start()
            st.success(f"Server started on port {st.session_state.custom_server_port}")
        else:
            st.warning("Server is already running.")
    else:
        stop_server()


def copy_xml_to_static():
    """Ensure XML is copied to Streamlit static directory."""
    if uglyfeeds_dir.exists() and (uglyfeeds_dir / uglyfeed_file).exists():
        destination_path = static_dir / uglyfeed_file
        shutil.copy(uglyfeeds_dir / uglyfeed_file, destination_path)
        return destination_path
    return None

def list_markdown_files(docs_dir):
    """List all Markdown files in the docs directory."""
    return [file for file in docs_dir.glob("*.md")]

def get_xml_stats():
    """Get quick stats from the XML file."""
    if not (uglyfeeds_dir / uglyfeed_file).exists():
        return None, None, None
    tree = ET.parse(uglyfeeds_dir / uglyfeed_file)
    root = tree.getroot()
    items = root.findall(".//item")
    item_count = len(items)
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item_count, last_updated, uglyfeeds_dir / uglyfeed_file

def get_xml_item_count():
    """Get the current count of items in the XML."""
    if not (uglyfeeds_dir / uglyfeed_file).exists():
        return 0
    tree = ET.parse(uglyfeeds_dir / uglyfeed_file)
    root = tree.getroot()
    items = root.findall(".//item")
    return len(items)

def get_new_item_count(old_count):
    """Calculate the new items count based on the old count."""
    new_count = get_xml_item_count()
    if old_count is None or new_count is None:
        return 0
    return new_count - old_count

def schedule_jobs(interval, period):
    """Schedule jobs to run periodically."""
    def job():
        run_scripts_sequentially()
        job_stats_global.append({
            'script': 'Scheduled Job',
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Success'
        })

    if period == 'minutes':
        schedule.every(interval).minutes.do(job)
    elif period == 'hours':
        schedule.every(interval).hours.do(job)
    elif period == 'days':
        schedule.every(interval).days.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Initialize session state
if 'config_data' not in st.session_state:
    st.session_state.config_data = ensure_default_config(load_config())
if 'server_thread' not in st.session_state:
    st.session_state.server_thread = None

# Load RSS feeds
if 'feeds' not in st.session_state:
    if feeds_path.exists():
        with open(feeds_path, "r") as f:
            st.session_state.feeds = f.read()
    else:
        st.session_state.feeds = ""

# Start scheduling if enabled in the config
if st.session_state.config_data.get('scheduling_enabled', False):
    scheduling_thread = threading.Thread(target=schedule_jobs, args=(st.session_state.config_data['scheduling_interval'], st.session_state.config_data['scheduling_period']), daemon=True)
    scheduling_thread.start()

# Sidebar navigation
st.sidebar.title("Navigation")
menu_options = [
    "Introduction",
    "Configuration",
    "Run Scripts",
    "View and Serve XML",
    "Deploy",
    "Debug"
]
selected_option = st.sidebar.selectbox("Select an option", menu_options)

# Ensure Font Awesome is included
st.sidebar.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <hr>
    <a href="https://github.com/fabriziosalmi/UglyFeed" target="_blank">
        <i class="fab fa-github" style="font-size: 32px;"></i>
    </a>
    """, unsafe_allow_html=True)


# Introduction Page
if selected_option == "Introduction":
    # Add title with GitHub icon on the left
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <img src="https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed.png?raw=true"
             alt="GitHub" style="width: 48px; height: 48px; margin-right: 10px;">
        <h1 style="margin: 0; display: inline; font-size: 2em;">UglyFeed</h1>
    </div>
    """, unsafe_allow_html=True)

    # Description with styled markdown
    st.markdown("""
    <p style="font-size: 16px; line-height: 1.6; text-align: justify;">
        This application provides a graphical user interface to manage and process RSS feeds using the UglyFeed project.
        Use the sidebar to navigate through different functionalities of the application:
    </p>
    <ul style="font-size: 16px; line-height: 1.6; margin-left: 20px;">
        <li><b>Configuration</b>: Set up and save your RSS feeds and processing options.</li>
        <li><b>Run Scripts</b>: Execute various processing scripts like <code>main.py</code>, <code>llm_processor.py</code>, and <code>json2rss.py</code> with just one click.</li>
        <li><b>View and Serve XML</b>: View the content of the XML feed and serve it via a custom HTTP server.</li>
        <li><b>Deploy</b>: Deploy the generated uglyfeed.xml file to GitHub and GitLab.</li>
        <li><b>Debug</b>: View detailed debug information for troubleshooting.</li>
    </ul>
    <p style="font-size: 16px; line-height: 1.6;">
        Ensure your local environment is correctly set up and necessary directories and files are in place.
        For any issues, <a href="https://github.com/fabriziosalmi/UglyFeed/issues/new/choose" target="_blank">open an issue on GitHub</a>. Enjoy!
    </p>
    """, unsafe_allow_html=True)


elif selected_option == "Configuration":
    st.header("Configuration")

    st.divider()

    st.subheader("RSS Feeds")
    st.session_state.feeds = st.text_area("Enter one RSS feed URL per line:", st.session_state.feeds)

    st.divider()

    # Preprocessing Options
    st.subheader("Preprocessing Options")
    st.session_state.config_data['preprocessing']['remove_html'] = st.checkbox("Remove HTML Tags", value=st.session_state.config_data['preprocessing']['remove_html'])
    st.session_state.config_data['preprocessing']['lowercase'] = st.checkbox("Convert to Lowercase", value=st.session_state.config_data['preprocessing']['lowercase'])
    st.session_state.config_data['preprocessing']['remove_punctuation'] = st.checkbox("Remove Punctuation", value=st.session_state.config_data['preprocessing']['remove_punctuation'])
    st.session_state.config_data['preprocessing']['lemmatization'] = st.checkbox("Apply Lemmatization", value=st.session_state.config_data['preprocessing']['lemmatization'])
    st.session_state.config_data['preprocessing']['stop_words'] = st.text_input("Stop Words Language", st.session_state.config_data['preprocessing']['stop_words'])
    st.session_state.config_data['preprocessing']['use_stemming'] = st.checkbox("Use Stemming", value=st.session_state.config_data['preprocessing']['use_stemming'])

    # Handle additional stopwords input and splitting
    additional_stopwords = ", ".join(st.session_state.config_data['preprocessing']['additional_stopwords'])
    additional_stopwords_input = st.text_input("Additional Stopwords (comma separated)", additional_stopwords).strip()
    st.session_state.config_data['preprocessing']['additional_stopwords'] = [word.strip() for word in additional_stopwords_input.split(",") if word.strip()]

    st.session_state.config_data['preprocessing']['min_word_length'] = st.number_input("Minimum Word Length", min_value=1, value=st.session_state.config_data['preprocessing']['min_word_length'])

    st.divider()

    # Vectorization Options
    st.subheader("Vectorization Options")
    vectorization_methods = ["tfidf", "count", "hashing"]
    selected_method = st.selectbox("Vectorization Method", vectorization_methods, index=vectorization_methods.index(st.session_state.config_data['vectorization']['method']))
    st.session_state.config_data['vectorization']['method'] = selected_method

    # Ensure ngram_range is handled as a list of two elements
    ngram_range = st.session_state.config_data['vectorization']['ngram_range']
    if isinstance(ngram_range, list) and len(ngram_range) == 2:
        st.session_state.config_data['vectorization']['ngram_range'] = st.slider("N-gram Range", 1, 5, (ngram_range[0], ngram_range[1]))
    else:
        st.session_state.config_data['vectorization']['ngram_range'] = st.slider("N-gram Range", 1, 5, (1, 2))

    st.session_state.config_data['vectorization']['max_df'] = st.slider("Max Document Frequency (max_df)", 0.0, 1.0, st.session_state.config_data['vectorization']['max_df'])
    st.session_state.config_data['vectorization']['min_df'] = st.slider("Min Document Frequency (min_df)", 0.0, 1.0, st.session_state.config_data['vectorization']['min_df'])
    st.session_state.config_data['vectorization']['max_features'] = st.number_input("Max Features", min_value=1, value=st.session_state.config_data['vectorization']['max_features'])


    st.divider()

    st.subheader("RSS Feed Details")
    st.session_state.config_data['feed_title'] = st.text_input("Feed Title", st.session_state.config_data['feed_title'])
    st.session_state.config_data['feed_link'] = st.text_input("Feed Link", st.session_state.config_data['feed_link'])
    st.session_state.config_data['feed_description'] = st.text_input("Feed Description", st.session_state.config_data['feed_description'])
    st.session_state.config_data['feed_language'] = st.text_input("Feed Language", st.session_state.config_data['feed_language'])
    st.session_state.config_data['feed_self_link'] = st.text_input("Feed Self-Link", st.session_state.config_data['feed_self_link'])
    st.session_state.config_data['author'] = st.text_input("Author", st.session_state.config_data['author'])
    st.session_state.config_data['category'] = st.text_input("Category", st.session_state.config_data['category'])
    st.session_state.config_data['copyright'] = st.text_input("Copyright", st.session_state.config_data['copyright'])

    st.divider()

    st.subheader("Similarity Options")
    st.session_state.config_data['similarity_threshold'] = st.slider("Similarity Threshold", 0.0, 1.0, st.session_state.config_data['similarity_threshold'])
    st.session_state.config_data['similarity_options']['min_samples'] = st.number_input("Minimum Samples", min_value=1, value=st.session_state.config_data['similarity_options']['min_samples'])
    st.session_state.config_data['similarity_options']['eps'] = st.number_input("Epsilon (eps)", min_value=0.0, value=st.session_state.config_data['similarity_options']['eps'], step=0.01)

    st.divider()

    st.subheader("API and LLM Options")
    api_options = ["OpenAI", "Groq", "Ollama"]
    selected_api = st.selectbox("Select API", api_options, index=api_options.index(st.session_state.config_data['api_config']['selected_api']))
    st.session_state.config_data['api_config']['selected_api'] = selected_api

    if selected_api == "OpenAI":
        st.session_state.config_data['api_config']['openai_api_url'] = st.text_input("OpenAI API URL", st.session_state.config_data['api_config']['openai_api_url'])
        st.session_state.config_data['api_config']['openai_api_key'] = st.text_input("OpenAI API Key", st.session_state.config_data['api_config']['openai_api_key'], type="password")
        st.session_state.config_data['api_config']['openai_model'] = st.text_input("OpenAI Model", st.session_state.config_data['api_config']['openai_model'])
    elif selected_api == "Groq":
        st.session_state.config_data['api_config']['groq_api_url'] = st.text_input("Groq API URL", st.session_state.config_data['api_config']['groq_api_url'])
        st.session_state.config_data['api_config']['groq_api_key'] = st.text_input("Groq API Key", st.session_state.config_data['api_config']['groq_api_key'], type="password")
        st.session_state.config_data['api_config']['groq_model'] = st.text_input("Groq Model", st.session_state.config_data['api_config']['groq_model'])
    else:
        st.session_state.config_data['api_config']['ollama_api_url'] = st.text_input("Ollama API URL", st.session_state.config_data['api_config']['ollama_api_url'])
        st.session_state.config_data['api_config']['ollama_model'] = st.text_input("Ollama Model", st.session_state.config_data['api_config']['ollama_model'])

    st.divider()

    st.subheader("Content Prefix")
    st.session_state.config_data['content_prefix'] = st.text_area("Content Prefix", st.session_state.config_data['content_prefix'])

    st.divider()

    st.subheader("RSS Retention Options")
    st.session_state.config_data['max_items'] = st.number_input("Maximum Items", min_value=1, value=st.session_state.config_data['max_items'])
    st.session_state.config_data['max_age_days'] = st.number_input("Maximum Age (days)", min_value=1, value=st.session_state.config_data['max_age_days'])

    st.divider()

    st.subheader("Scheduling Options")
    scheduling_enabled = st.session_state.config_data.get('scheduling_enabled', False)
    st.session_state.config_data['scheduling_enabled'] = st.checkbox("Enable Scheduled Execution", value=scheduling_enabled)

    interval_options = {
        "2 minutes": (2, 'minutes'),
        "10 minutes": (10, 'minutes'),
        "30 minutes": (30, 'minutes'),
        "1 hour": (1, 'hours'),
        "4 hours": (4, 'hours'),
        "12 hours": (12, 'hours'),
        "24 hours": (24, 'hours')
    }
    default_interval = next((k for k, v in interval_options.items() if v == (st.session_state.config_data.get('scheduling_interval', 2), st.session_state.config_data.get('scheduling_period', 'minutes'))), "2 minutes")
    selected_interval = st.selectbox("Select Scheduling Interval", list(interval_options.keys()), index=list(interval_options.keys()).index(default_interval))

    interval, period = interval_options[selected_interval]
    st.session_state.config_data['scheduling_interval'] = interval
    st.session_state.config_data['scheduling_period'] = period

    st.subheader("HTTP Server Configuration")
    st.session_state.config_data['http_server_port'] = st.number_input("HTTP Server Port", min_value=1, max_value=65535, value=st.session_state.config_data['http_server_port'])

    st.divider()

    if st.button("Save Configuration and Feeds"):
        save_configuration()


# Run Scripts Section
elif selected_option == "Run Scripts":
    st.header("Run Scripts")

    # Add example text or instructions
    st.markdown("""
    This section allows you to run the necessary scripts to process and generate the RSS feed.

    - **main.py** retrieves the RSS feeds and prepares the data for further processing.
    - **llm_processor.py** uses the Large Language Model to rewrite and enhance the feed content.
    - **json2rss.py** converts the processed and rewritten JSON data into a valid RSS feed.

    Output and errors are shown for each scripts for debugging purpose.

    """)

    # Run the scripts sequentially
    if st.button("Run main.py, llm_processor.py, and json2rss.py sequentially"):
        run_scripts_sequentially()


# View and Serve XML Section
elif selected_option == "View and Serve XML":
    st.header("View and Serve XML")

    xml_file_path = copy_xml_to_static()
    if not xml_file_path:
        st.warning(f"The file '{uglyfeed_file}' does not exist in the directory '{uglyfeeds_dir}'.")
    else:
        with open(xml_file_path, "r") as f:
            xml_content = f.read()
        st.text_area("XML Content", xml_content, height=300)

        with open(xml_file_path, "rb") as f:
            st.download_button(
                label="Download XML File",
                data=f,
                file_name=uglyfeed_file,
                mime="application/xml"
            )

        st.subheader("Control HTTP Server for XML Serving")
        if st.button("Start HTTP Server"):
            toggle_server(True)
        if st.button("Stop HTTP Server"):
            toggle_server(False)

        if st.session_state.server_thread and st.session_state.server_thread.is_alive():
            local_ip = get_local_ip()
            serve_url = f"http://{local_ip}:{st.session_state.custom_server_port}/{uglyfeed_file}"
            st.markdown(f"**Serving `{uglyfeed_file}` at:**\n\n[{serve_url}]({serve_url})")
        else:
            st.info("Server is not running.")


# Import the deploy function from deploy_xml.py
from deploy_xml import deploy_xml, load_config

# Deploy Section
if selected_option == "Deploy":
    st.header("Deploy XML File")

    # Load configuration
    config = load_config()

    st.write("This section allows you to deploy the `uglyfeed.xml` file to GitHub and GitLab.")
    st.write("Current configuration:")
    st.json(config)

    # Button to start deployment
    if st.button("Deploy to GitHub and GitLab"):
        try:
            with st.spinner("Deploying..."):
                # Deploy the XML file
                urls = deploy_xml('uglyfeeds/uglyfeed.xml', config)

                if urls:
                    st.success("Deployment successful!")
                    st.write("File deployed to the following URLs:")
                    for platform, url in urls.items():
                        st.markdown(f"**{platform.capitalize()}**: [View]({url})")

                    # Store the deployment URLs in session state
                    st.session_state['urls'] = urls
                else:
                    st.warning("No deployments were made. Check if the configuration is correct.")
        except Exception as e:
            st.error(f"An error occurred during deployment: {e}")

    # Display previous deployment status if available
    st.subheader("Previous Deployment Status")
    if 'urls' in st.session_state:
        st.write("Last deployed to the following URLs:")
        for platform, url in st.session_state['urls'].items():
            st.markdown(f"**{platform.capitalize()}**: [View]({url})")
    else:
        st.info("No previous deployments found.")



# Debug Section
elif selected_option == "Debug":
    st.header("Debug")

    # Job Execution Logs
    st.subheader("Job Execution Logs")
    if job_stats_global:
        with st.expander("View Detailed Logs"):
            for stat in job_stats_global:
                status_color = "green" if stat['status'].lower() == 'success' else "red"
                st.markdown(f"<div style='background-color: {status_color}; padding: 10px; border-radius: 5px;'>"
                            f"<strong>Script:</strong> `{stat['script']}`<br>"
                            f"<strong>Time:</strong> `{stat['time']}`<br>"
                            f"<strong>Status:</strong> `{stat['status']}`<br>"
                            f"<strong>New Items:</strong> `{stat.get('new_items', 0)}`"
                            f"</div>", unsafe_allow_html=True)
                st.divider()
    else:
        st.info("No job executions have been recorded yet.")

    # XML File Stats
    st.subheader("XML File Stats")
    item_count, last_updated, xml_path = get_xml_stats()
    if item_count is not None:
        with st.expander("View XML File Details"):
            st.write(f"**Item Count:** `{item_count}`")
            st.write(f"**Last Updated:** `{last_updated}`")
            st.write(f"**File Path:** `{xml_path}`")
    else:
        st.warning("No XML file found or file is empty. Please ensure the XML file is generated properly.")

    # Check if HTTP server on port 8001 is running
    st.subheader("HTTP Server Status (Port 8001)")
    try:
        response = requests.get('http://localhost:8001', timeout=5)
        if response.status_code == 200:
            st.success("HTTP server on port 8001 is running.")
        else:
            st.warning("HTTP server on port 8001 is not responding as expected.")
    except requests.ConnectionError:
        st.error("HTTP server on port 8001 is not running.")

    # System Information
    st.subheader("System Information")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    st.write(f"**Hostname:** `{hostname}`")
    st.write(f"**IP Address:** `{ip_address}`")
    st.write(f"**CPU Usage:** `{cpu_usage}%`")
    st.write(f"**Memory Usage:** `{memory_info.percent}%` (Available: `{memory_info.available // (1024 ** 2)} MB`)")

    # Current Configuration
    st.subheader("Current Configuration")
    with st.expander("View Config.yaml Content"):
        st.text_area("Config.yaml Content", yaml.dump(st.session_state.config_data), height=300)
        if st.button("Refresh Configuration"):
            # Code to refresh configuration can be placed here
            st.experimental_rerun()  # This will refresh the Streamlit app

    # Loaded Feeds
    st.subheader("Loaded Feeds")
    with st.expander("View Feeds Content"):
        st.text_area("Feeds Content", st.session_state.feeds, height=200)
        if st.button("Refresh Feeds"):
            # Code to refresh feeds can be placed here
            st.experimental_rerun()  # This will refresh the Streamlit app

    # Download Logs
    st.subheader("Download Logs")
    logs_path = Path('logs.txt')
    if logs_path.exists():
        with logs_path.open('r') as log_file:
            logs = log_file.read()
        st.download_button('Download Log File', logs, file_name='logs.txt')
        st.text_area("Log File Content", logs, height=300)
    else:
        st.warning("No log file found. Please ensure logs are being recorded properly.")

    # Log Level Slider
    st.subheader("Adjust Log Level")
    log_level = st.select_slider(
        "Select log level",
        options=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        value="INFO"
    )
    logger.setLevel(log_level)
    st.info(f"Current log level set to: {log_level}")

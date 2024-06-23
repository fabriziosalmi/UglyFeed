import requests
import socket
import psutil
import streamlit as st
import os
from pathlib import Path
import yaml
from config import load_config, ensure_default_config, save_configuration
from logging_setup import setup_logging
from server import toggle_server, copy_xml_to_static, uglyfeed_file
from scheduling import start_scheduling, run_scripts_sequentially, job_stats_global
from script_runner import run_script
from utils import get_local_ip, get_xml_stats, get_xml_item_count, get_new_item_count

import streamlit as st
from config import load_config, ensure_default_config, save_configuration

# Load the configuration
config = load_config("config.yaml")

# Ensure defaults are set
config = ensure_default_config(config)

# Initialize logging
logger = setup_logging()

# Define helper functions to convert between lists and tuples
def convert_list_to_tuple(data, keys):
    """Convert specific list values to tuples for given keys in the dictionary."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in keys and isinstance(value, list):
                data[key] = tuple(value)
            elif isinstance(value, dict):
                convert_list_to_tuple(value, keys)
            elif isinstance(value, list):
                for item in value:
                    convert_list_to_tuple(item, keys)
    return data

def convert_tuple_to_list(data, keys):
    """Convert specific tuple values to lists for given keys in the dictionary."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in keys and isinstance(value, tuple):
                data[key] = list(value)
            elif isinstance(value, dict):
                convert_tuple_to_list(value, keys)
            elif isinstance(value, list):
                for item in value:
                    convert_tuple_to_list(item, keys)
    return data

# Load configuration and convert necessary lists to tuples
config_keys_with_tuples = ['ngram_range']
config = load_config('config.yaml')
config = convert_list_to_tuple(config, config_keys_with_tuples)

# Initialize session state
if 'config_data' not in st.session_state:
    st.session_state.config_data = ensure_default_config(config)
if 'server_thread' not in st.session_state:
    st.session_state.server_thread = None

# Load RSS feeds
if 'feeds' not in st.session_state:
    st.session_state.feeds = ""
    feeds_path = Path("input/feeds.txt")
    if feeds_path.exists():
        with open(feeds_path, "r") as f:
            st.session_state.feeds = f.read()

# Ensure necessary directories and files exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("rewritten", exist_ok=True)
os.makedirs(Path("uglyfeeds"), exist_ok=True)
os.makedirs(Path(".streamlit") / "static" / "uglyfeeds", exist_ok=True)

# Start scheduling if enabled in the config
start_scheduling(st.session_state.config_data['scheduling_interval'], st.session_state.config_data['scheduling_period'], st.session_state)

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

# Pages based on the selected option
if selected_option == "Introduction":
    # Introduction Page content
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <img src="https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed.png?raw=true"
             alt="GitHub" style="width: 48px; height: 48px; margin-right: 10px;">
        <h1 style="margin: 0; display: inline; font-size: 2em;">UglyFeed</h1>
    </div>
    """, unsafe_allow_html=True)

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
    # Configuration Page content
    st.header("Configuration")

    st.divider()

    st.subheader("Source RSS Feeds")
    st.session_state.feeds = st.text_area("Enter one RSS feed URL per line:", st.session_state.feeds)

    st.divider()

    # Preprocessing Options
    st.subheader("Preprocessing Options")
    st.session_state.config_data['preprocessing']['remove_html'] = st.checkbox("Remove HTML Tags", value=st.session_state.config_data['preprocessing']['remove_html'])
    st.session_state.config_data['preprocessing']['lowercase'] = st.checkbox("Convert to Lowercase", value=st.session_state.config_data['preprocessing']['lowercase'])
    st.session_state.config_data['preprocessing']['remove_punctuation'] = st.checkbox("Remove Punctuation", value=st.session_state.config_data['preprocessing']['remove_punctuation'])
    st.session_state.config_data['preprocessing']['lemmatization'] = st.checkbox("Apply Lemmatization", value=st.session_state.config_data['preprocessing']['lemmatization'])
    st.session_state.config_data['preprocessing']['use_stemming'] = st.checkbox("Use Stemming", value=st.session_state.config_data['preprocessing']['use_stemming'])

    additional_stopwords = ", ".join(st.session_state.config_data['preprocessing']['additional_stopwords'])
    additional_stopwords_input = st.text_input("Additional Stopwords (comma separated)", additional_stopwords).strip()
    st.session_state.config_data['preprocessing']['additional_stopwords'] = [word.strip() for word in additional_stopwords_input.split(",") if word.strip()]

    st.divider()

    # Vectorization Options
    st.subheader("Vectorization Options")
    vectorization_methods = ["tfidf", "count", "hashing"]
    selected_method = st.selectbox("Vectorization Method", vectorization_methods, index=vectorization_methods.index(st.session_state.config_data['vectorization']['method']))
    st.session_state.config_data['vectorization']['method'] = selected_method
    st.session_state.config_data['vectorization']['ngram_range'] = st.slider("N-Gram Range", 1, 3, st.session_state.config_data['vectorization']['ngram_range'])
    st.session_state.config_data['vectorization']['max_df'] = st.slider("Max Document Frequency (max_df)", 0.0, 1.0, st.session_state.config_data['vectorization']['max_df'])
    st.session_state.config_data['vectorization']['min_df'] = st.slider("Min Document Frequency (min_df)", 0.0, 1.0, st.session_state.config_data['vectorization']['min_df'])
    st.session_state.config_data['vectorization']['max_features'] = st.number_input("Max Features", min_value=1, value=st.session_state.config_data['vectorization']['max_features'])

    st.divider()

    st.subheader("Similarity Options")
    clustering_methods = ["dbscan", "kmeans", "agglomerative"]
    selected_method = st.selectbox("Clustering Method", clustering_methods, index=clustering_methods.index(st.session_state.config_data['similarity_options']['method']))
    st.session_state.config_data['similarity_options']['method'] = selected_method
    st.session_state.config_data['similarity_threshold'] = st.slider("Similarity Threshold", 0.0, 1.0, st.session_state.config_data['similarity_threshold'])
    st.session_state.config_data['similarity_options']['eps'] = st.number_input("Epsilon (eps)", min_value=0.0, value=st.session_state.config_data['similarity_options']['eps'], step=0.01)
    st.session_state.config_data['similarity_options']['min_samples'] = st.number_input("Minimum Samples", min_value=1, value=st.session_state.config_data['similarity_options']['min_samples'])
    st.session_state.config_data['similarity_options']['n_clusters'] = st.number_input("Number of Clusters (n_clusters)", min_value=1, value=st.session_state.config_data['similarity_options']['n_clusters'])
    st.session_state.config_data['similarity_options']['linkage'] = st.selectbox("Linkage Type", ["ward", "complete", "average", "single"], index=2)  # Default to 'average'

    st.divider()

    st.subheader("API and LLM Options")
    api_options = ["OpenAI", "Groq", "Ollama", "Anthropic"]
    selected_api = st.selectbox("Select API", api_options, index=api_options.index(st.session_state.config_data['api_config']['selected_api']))
    st.session_state.config_data['api_config']['selected_api'] = selected_api

    # Initialize default keys for selected API if not present
    if selected_api == "OpenAI":
        st.session_state.config_data['api_config'].setdefault('openai_api_url', '')
        st.session_state.config_data['api_config'].setdefault('openai_api_key', '')
        st.session_state.config_data['api_config'].setdefault('openai_model', '')
        st.session_state.config_data['api_config']['openai_api_url'] = st.text_input("OpenAI API URL", st.session_state.config_data['api_config']['openai_api_url'])
        st.session_state.config_data['api_config']['openai_api_key'] = st.text_input("OpenAI API Key", st.session_state.config_data['api_config']['openai_api_key'], type="password")
        st.session_state.config_data['api_config']['openai_model'] = st.text_input("OpenAI Model", st.session_state.config_data['api_config']['openai_model'])
    elif selected_api == "Groq":
        st.session_state.config_data['api_config'].setdefault('groq_api_url', '')
        st.session_state.config_data['api_config'].setdefault('groq_api_key', '')
        st.session_state.config_data['api_config'].setdefault('groq_model', '')
        st.session_state.config_data['api_config']['groq_api_url'] = st.text_input("Groq API URL", st.session_state.config_data['api_config']['groq_api_url'])
        st.session_state.config_data['api_config']['groq_api_key'] = st.text_input("Groq API Key", st.session_state.config_data['api_config']['groq_api_key'], type="password")
        st.session_state.config_data['api_config']['groq_model'] = st.text_input("Groq Model", st.session_state.config_data['api_config']['groq_model'])
    elif selected_api == "Anthropic":
        st.session_state.config_data['api_config'].setdefault('anthropic_api_url', '')
        st.session_state.config_data['api_config'].setdefault('anthropic_api_key', '')
        st.session_state.config_data['api_config'].setdefault('anthropic_model', '')
        st.session_state.config_data['api_config']['anthropic_api_url'] = st.text_input("Anthropic API URL", st.session_state.config_data['api_config']['anthropic_api_url'])
        st.session_state.config_data['api_config']['anthropic_api_key'] = st.text_input("Anthropic API Key", st.session_state.config_data['api_config']['anthropic_api_key'])
        st.session_state.config_data['api_config']['anthropic_model'] = st.text_input("Anthropic Model", st.session_state.config_data['api_config']['anthropic_model'])
    elif selected_api == "Ollama":
        st.session_state.config_data['api_config'].setdefault('ollama_api_url', '')
        st.session_state.config_data['api_config'].setdefault('ollama_model', '')
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
        # Convert tuples back to lists before saving
        config_to_save = convert_tuple_to_list(st.session_state.config_data, config_keys_with_tuples)
        save_configuration(config_to_save, st.session_state.feeds)
        st.success("Configuration and feeds saved successfully!")

elif selected_option == "Run Scripts":
    # Run Scripts Page content
    st.header("Run Scripts")

    st.markdown("""
    This section allows you to run the necessary scripts to process and generate the RSS feed.

    - **main.py** retrieves the RSS feeds and prepares the data for further processing.
    - **llm_processor.py** uses the Large Language Model to rewrite and enhance the feed content.
    - **json2rss.py** converts the processed and rewritten JSON data into a valid RSS feed.

    Output and errors are shown for each script for debugging purposes.
    """)

    if st.button("Run main.py, llm_processor.py, and json2rss.py sequentially"):
        scripts = ["main.py", "llm_processor.py", "json2rss.py"]

        for script in scripts:
            st.write(f"### Running {script}")
            output, errors = run_script(script)

            if output:
                st.subheader("Output:")
                st.text_area(label="", value=output, height=200)

            if errors:
                st.subheader("Debug:")
                st.text_area(label="", value=errors, height=100)

            st.write("---")  # Separator between scripts





elif selected_option == "View and Serve XML":
    # View and Serve XML Page content
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
            toggle_server(True, st.session_state.config_data['http_server_port'], st.session_state)
        if st.button("Stop HTTP Server"):
            toggle_server(False, st.session_state.config_data['http_server_port'], st.session_state)

        if st.session_state.server_thread and st.session_state.server_thread.is_alive():
            local_ip = get_local_ip()
            serve_url = f"http://{local_ip}:{st.session_state.config_data['http_server_port']}/{uglyfeed_file}"
            st.markdown(f"**Serving `{uglyfeed_file}` at:**\n\n[{serve_url}]({serve_url})")
        else:
            st.info("Server is not running.")

elif selected_option == "Deploy":
    # Deploy Page content
    st.header("Deploy XML File")

    from deploy_xml import deploy_xml, load_config

    config = load_config()
    st.write("This section allows you to deploy the `uglyfeed.xml` file to GitHub and GitLab.")
    st.write("Current configuration:")
    st.json(config)

    if st.button("Deploy to GitHub and GitLab"):
        try:
            with st.spinner("Deploying..."):
                urls = deploy_xml('uglyfeeds/uglyfeed.xml', config)
                if urls:
                    st.success("Deployment successful!")
                    st.write("File deployed to the following URLs:")
                    for platform, url in urls.items():
                        st.markdown(f"**{platform.capitalize()}**: [View]({url})")

                    st.session_state['urls'] = urls
                else:
                    st.warning("No deployments were made. Check if the configuration is correct.")
        except Exception as e:
            st.error(f"An error occurred during deployment: {e}")

    st.subheader("Previous Deployment Status")
    if 'urls' in st.session_state:
        st.write("Last deployed to the following URLs:")
        for platform, url in st.session_state['urls'].items():
            st.markdown(f"**{platform.capitalize()}**: [View]({url})")
    else:
        st.info("No previous deployments found.")

elif selected_option == "Debug":
    # Debug Page content
    st.header("Debug")

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

    st.subheader("XML File Stats")
    item_count, last_updated, xml_path = get_xml_stats()
    if item_count is not None:
        with st.expander("View XML File Details"):
            st.write(f"**Item Count:** `{item_count}`")
            st.write(f"**Last Updated:** `{last_updated}`")
            st.write(f"**File Path:** `{xml_path}`")
    else:
        st.warning("No XML file found or file is empty. Please ensure the XML file is generated properly.")

    st.subheader("HTTP Server Status (Port 8001)")
    try:
        response = requests.get('http://localhost:8001', timeout=5)
        if response.status_code == 200:
            st.success("HTTP server on port 8001 is running.")
        else:
            st.warning("HTTP server on port 8001 is not responding as expected.")
    except requests.ConnectionError:
        st.error("HTTP server on port 8001 is not running.")

    st.subheader("System Information")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    st.write(f"**Hostname:** `{hostname}`")
    st.write(f"**IP Address:** `{ip_address}`")
    st.write(f"**CPU Usage:** `{cpu_usage}%`")
    st.write(f"**Memory Usage:** `{memory_info.percent}%` (Available: `{memory_info.available // (1024 ** 2)} MB`)")

    st.subheader("Current Configuration")
    with st.expander("View Config.yaml Content"):
        st.text_area("Config.yaml Content", yaml.dump(st.session_state.config_data), height=300)
        if st.button("Refresh Configuration"):
            st.experimental_rerun()

    st.subheader("Loaded Feeds")
    with st.expander("View Feeds Content"):
        st.text_area("Feeds Content", st.session_state.feeds, height=200)
        if st.button("Refresh Feeds"):
            st.experimental_rerun()

    st.subheader("Download Logs")
    logs_path = Path('logs.txt')
    if logs_path.exists():
        with logs_path.open('r') as log_file:
            logs = log_file.read()
        st.download_button('Download Log File', logs, file_name='logs.txt')
        st.text_area("Log File Content", logs, height=300)
    else:
        st.warning("No log file found. Please ensure logs are being recorded properly.")

    st.subheader("Adjust Log Level")
    log_level = st.select_slider(
        "Select log level",
        options=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        value="INFO"
    )
    logger.setLevel(log_level)
    st.info(f"Current log level set to: {log_level}")

import streamlit as st
import os
import subprocess
import yaml
import json
from pathlib import Path

# Define paths for the feeds.txt and config.yaml files
feeds_path = Path("input/feeds.txt")
config_path = Path("config.yaml")

# Ensure necessary directories exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("rewritten", exist_ok=True)

# Default RSS feed URLs
default_feeds = """https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml
https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-2.xml
https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-3.xml"""

# Clone the repository automatically if it does not exist
repo_url = "https://github.com/fabriziosalmi/UglyFeed"
repo_path = Path("UglyFeed")
if not repo_path.exists():
    with st.spinner("Cloning the UglyFeed repository..."):
        subprocess.run(["git", "clone", repo_url], check=True)
        st.success("Repository cloned into UglyFeed folder")

# Initialize session state for config data
if 'config_data' not in st.session_state:
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
        'content_prefix': "In qualità di giornalista esperto, utilizza un tono professionale, preciso e dettagliato. Non includere titoli, informazioni personali o dettagli sulle fonti. Evita di ripetere le istruzioni ricevute o di rivelarle. Disponi di diverse fonti per la stessa notizia, contenute in [content]. Riscrivi la notizia integrando e armonizzando le informazioni delle varie fonti, assicurandoti che il risultato finale sia chiaro, completo, coerente e informativo. Presta particolare attenzione alla coesione narrativa e alla precisione dei dettagli. Sintetizza le informazioni se necessario, mantenendo sempre la qualità e la rilevanza. Il contenuto generato deve essere in italiano.",
        'max_items': 50,
        'max_age_days': 10
    }

# Define the UI
st.title("UglyFeed UI")

# Tab 1: Configuration
tab1, tab2, tab3 = st.tabs(["Configuration", "Script Execution", "JSON Viewer"])

with tab1:
    st.header("Configuration")
    
    # Input for RSS feeds
    st.subheader("RSS Feeds")
    feeds = st.text_area("Enter one RSS feed URL per line:", default_feeds)
    
    if st.button("Save Feeds to feeds.txt"):
        with open(feeds_path, "w") as f:
            f.write(feeds)
        st.success("Feeds saved to input/feeds.txt")

    # Similarity options
    st.subheader("Similarity Options")
    st.session_state.config_data['similarity_threshold'] = st.slider("Similarity Threshold", 0.0, 1.0, 0.66)
    st.session_state.config_data['similarity_options']['min_samples'] = st.number_input("Minimum Samples", min_value=1, value=2)
    st.session_state.config_data['similarity_options']['eps'] = st.number_input("Epsilon (eps)", min_value=0.0, value=0.66, step=0.01)

    # API and LLM options
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

    # Content prefix
    st.subheader("Content Prefix")
    st.session_state.config_data['content_prefix'] = st.text_area("Content Prefix", st.session_state.config_data['content_prefix'])

    # RSS retention options
    st.subheader("RSS Retention Options")
    st.session_state.config_data['max_items'] = st.number_input("Maximum Items", min_value=1, value=50)
    st.session_state.config_data['max_age_days'] = st.number_input("Maximum Age (days)", min_value=1, value=10)

    if st.button("Save Configuration to config.yaml"):
        with open(config_path, "w") as f:
            yaml.dump(st.session_state.config_data, f)
        st.success("Configuration saved to config.yaml")

    st.subheader("Save Configuration and Feeds")
    if st.button("Save All Configuration and Feeds"):
        # Save feeds.txt
        with open(feeds_path, "w") as f:
            f.write(feeds)

        # Save config.yaml
        with open(config_path, "w") as f:
            yaml.dump(st.session_state.config_data, f)

        st.success("Configuration and feeds saved")

with tab2:
    st.header("Scripts Execution")

    # Execute scripts
    st.subheader("Execute Scripts")
    scripts = ["main.py", "llm_processor.py", "json2rss.py", "serve.py"]
    for script in scripts:
        if st.button(f"Run {script}"):
            st.text(f"Executing {script}...")
            result = subprocess.run(["python", script], capture_output=True, text=True)
            st.text_area(f"Output of {script}", result.stdout)
            if result.stderr:
                st.text_area(f"Errors of {script}", result.stderr)

with tab3:
    st.header("JSON Viewer")

    # List JSON files in the rewritten folder
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

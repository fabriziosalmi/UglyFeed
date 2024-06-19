import os
import argparse
import time
import yaml
import logging
import sys
import streamlit as st
from rss_reader import fetch_feeds_from_file
from similarity_checker import group_similar_articles
from json_manager import save_grouped_articles

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            logging.info(f"Loading configuration from {config_path}")
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Failed to load configuration from {config_path}: {e}")
        sys.exit(1)

def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(directory):
        logging.info(f"Creating missing directory: {directory}")
        os.makedirs(directory)

def merge_configs(default_config, env_config, cli_config):
    """Merge configurations with priority: CLI > ENV > default (YAML)."""
    merged_config = default_config.copy()
    
    # Update with environment variables if they are set
    for key, value in env_config.items():
        if value is not None:
            merged_config[key] = value

    # Update with command-line arguments if they are set
    for key, value in cli_config.items():
        if value is not None:
            merged_config[key] = value

    return merged_config

def main(config: dict) -> None:
    """Main function to process RSS feeds and group similar articles."""
    logging.info("Starting RSS feed processing...")
    input_file_path = 'input/feeds.txt'
    output_directory = config.get('folders', {}).get('output_folder', 'output')
    start_time = time.time()

    logging.info("Ensuring output directory exists...")
    ensure_directory_exists(output_directory)

    try:
        logging.info("Fetching and parsing RSS feeds...")
        articles = fetch_feeds_from_file(input_file_path)
        logging.info(f"Total articles fetched and parsed: {len(articles)}")
    except Exception as e:
        logging.error(f"Error fetching or parsing RSS feeds: {e}")
        return

    similarity_threshold = config.get('similarity_threshold', 0.66)
    similarity_options = config.get('similarity_options', {})

    with st.spinner('Grouping articles based on similarity...'):
        try:
            grouped_articles = group_similar_articles(articles, similarity_threshold, similarity_options)
            logging.info(f"Total groups formed: {len(grouped_articles)}")
        except Exception as e:
            logging.error(f"Error grouping articles by similarity: {e}")
            return

    logging.info("Saving grouped articles to JSON files...")
    try:
        group_sizes = save_grouped_articles(grouped_articles, output_directory)
        total_files_saved = len(group_sizes)
        logging.info(f"RSS feed processing complete. {total_files_saved} different articles are now grouped.")
        logging.info(f"Details of groups saved: {group_sizes}")
    except Exception as e:
        logging.error(f"Error saving grouped articles to JSON files: {e}")
        return

    elapsed_time = time.time() - start_time
    logging.info(f"(Took {elapsed_time:.2f} seconds)")

    logging.info("Summarizing output files:")
    try:
        output_files = os.listdir(output_directory)
        for filename in output_files:
            path = os.path.join(output_directory, filename)
            with open(path, 'r', encoding='utf-8') as file:
                line_count = sum(1 for _ in file)
            logging.info(f"{filename}: {line_count} lines")
        logging.info(f"Total output files: {len(output_files)}")
    except Exception as e:
        logging.error(f"Error summarizing output files: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process RSS feeds and group similar articles based on a similarity threshold.'
    )
    parser.add_argument(
        '-c', '--config', type=str, default='config.yaml',
        help='Path to the configuration file (default: config.yaml).'
    )
    parser.add_argument(
        '--similarity_threshold', type=float, help='Similarity threshold for grouping articles.'
    )
    parser.add_argument(
        '--min_samples', type=int, help='Minimum number of samples for DBSCAN clustering.'
    )
    parser.add_argument(
        '--eps', type=float, help='Maximum distance between samples for one to be considered as in the neighborhood of the other in DBSCAN.'
    )
    parser.add_argument(
        '--output_folder', type=str, help='Output folder for saving grouped articles.'
    )
    args = parser.parse_args()

    # Load default configuration from the YAML file
    config = load_config(args.config)

    # Override with environment variables if they exist
    env_config = {
        'similarity_threshold': float(os.getenv('SIMILARITY_THRESHOLD', config.get('similarity_threshold'))),
        'min_samples': int(os.getenv('MIN_SAMPLES', config.get('similarity_options', {}).get('min_samples', None))),
        'eps': float(os.getenv('EPS', config.get('similarity_options', {}).get('eps', None))),
        'output_folder': os.getenv('OUTPUT_FOLDER', config.get('folders', {}).get('output_folder', 'output'))
    }

    # Override with command-line arguments if provided
    cli_config = {
        'similarity_threshold': args.similarity_threshold,
        'min_samples': args.min_samples,
        'eps': args.eps,
        'output_folder': args.output_folder
    }

    # Merge all configurations with priority: CLI > ENV > YAML
    final_config = merge_configs(config, env_config, cli_config)

    # Update config dictionary with merged options
    if 'similarity_options' not in final_config:
        final_config['similarity_options'] = {}
    final_config['similarity_options']['min_samples'] = final_config.pop('min_samples', None)
    final_config['similarity_options']['eps'] = final_config.pop('eps', None)
    if 'folders' not in final_config:
        final_config['folders'] = {}
    final_config['folders']['output_folder'] = final_config.pop('output_folder', 'output')

    # Run the main function with the final merged configuration
    main(final_config)

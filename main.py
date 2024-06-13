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

def setup_logging():
    """Setup logging with separate handlers for info and error levels."""
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    # Handler for informational messages (stdout)
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)

    # Handler for error messages (stderr)
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(error_formatter)

    # Add handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger

logger = setup_logging()

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            logger.info(f"Loading configuration from {config_path}")
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load configuration from {config_path}: {e}")
        sys.exit(1)

def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(directory):
        logger.info(f"Creating missing directory: {directory}")
        os.makedirs(directory)

def main(config: dict) -> None:
    """Main function to process RSS feeds and group similar articles."""
    logger.info("Starting RSS feed processing...")
    input_file_path = 'input/feeds.txt'
    output_directory = 'output'
    start_time = time.time()

    logger.info("Ensuring output directory exists...")
    ensure_directory_exists(output_directory)

    try:
        logger.info("Fetching and parsing RSS feeds...")
        articles = fetch_feeds_from_file(input_file_path)
        logger.info(f"Total articles fetched and parsed: {len(articles)}")
    except Exception as e:
        logger.error(f"Error fetching or parsing RSS feeds: {e}")
        return

    similarity_threshold = config.get('similarity_threshold', 0.66)
    similarity_options = config.get('similarity_options', {})

    with st.spinner('Grouping articles based on similarity...'):
        try:
            grouped_articles = group_similar_articles(articles, similarity_threshold, similarity_options)
            logger.info(f"Total groups formed: {len(grouped_articles)}")
        except Exception as e:
            logger.error(f"Error grouping articles by similarity: {e}")
            return

    logger.info("Saving grouped articles to JSON files...")
    progress_bar = st.progress(0)  # Initialize the progress bar
    try:
        group_sizes = save_grouped_articles(grouped_articles, output_directory, progress_bar)
        total_files_saved = len(group_sizes)
        logger.info(f"RSS feed processing complete. {total_files_saved} different articles are now grouped.")
        logger.info(f"Details of groups saved: {group_sizes}")
    except Exception as e:
        logger.error(f"Error saving grouped articles to JSON files: {e}")
        return

    elapsed_time = time.time() - start_time
    logger.info(f"(Took {elapsed_time:.2f} seconds)")

    logger.info("Summarizing output files:")
    try:
        output_files = os.listdir(output_directory)
        for filename in output_files:
            path = os.path.join(output_directory, filename)
            with open(path, 'r', encoding='utf-8') as file:
                line_count = sum(1 for _ in file)
            logger.info(f"{filename}: {line_count} lines")
        logger.info(f"Total output files: {len(output_files)}")
    except Exception as e:
        logger.error(f"Error summarizing output files: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process RSS feeds and group similar articles based on a similarity threshold.'
    )
    parser.add_argument(
        '-c', '--config', type=str, default='config.yaml',
        help='Path to the configuration file (default: config.yaml).'
    )
    args = parser.parse_args()
    config = load_config(args.config)
    main(config)

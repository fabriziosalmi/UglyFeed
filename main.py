import os
import argparse
import time
import yaml
from rss_reader import fetch_feeds_from_file
from similarity_checker import group_similar_articles
from json_manager import save_grouped_articles

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(directory):
        print(f"Creating missing directory: {directory}")
        os.makedirs(directory)

def main(config: dict) -> None:
    """Main function to process RSS feeds and group similar articles."""
    print("Starting RSS feed processing...")
    input_file_path = 'input/feeds.txt'
    output_directory = 'output'
    start_time = time.time()

    print("Ensuring output directory exists...")
    ensure_directory_exists(output_directory)

    print("Fetching and parsing RSS feeds...")
    articles = fetch_feeds_from_file(input_file_path)
    print(f"Total articles fetched and parsed: {len(articles)}")

    similarity_threshold = config['similarity_threshold']
    similarity_options = config['similarity_options']

    print(f"Grouping articles based on similarity (threshold={similarity_threshold})...")
    grouped_articles = group_similar_articles(articles, similarity_threshold, similarity_options)
    print(f"Total groups formed: {len(grouped_articles)}")

    print("Saving grouped articles to JSON files...")
    group_sizes = save_grouped_articles(grouped_articles, output_directory)
    total_files_saved = len(group_sizes)

    elapsed_time = time.time() - start_time
    print(f"RSS feed processing complete. {total_files_saved} different articles are now grouped.")
    print(f"Details of groups saved: {group_sizes}")
    print(f"(Took {elapsed_time:.2f} seconds)")

    # Additional output to summarize file generation
    print("Summarizing output files:")
    output_files = os.listdir(output_directory)
    for filename in output_files:
        path = os.path.join(output_directory, filename)
        with open(path, 'r', encoding='utf-8') as file:
            line_count = sum(1 for _ in file)
        print(f"{filename}: {line_count} lines")
    print(f"Total output files: {len(output_files)}")

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

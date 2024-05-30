import xml.etree.ElementTree as ET
import requests
import os
import logging
import argparse
from urllib.parse import urlparse

def fetch_opml_from_url(url):
    """
    Fetches OPML content from a given URL.

    :param url: URL of the OPML file.
    :return: OPML content as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching OPML from URL: {e}")
        raise

def fetch_opml_from_file(filepath):
    """
    Fetches OPML content from a local file.

    :param filepath: Path to the local OPML file.
    :return: OPML content as a string.
    """
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except IOError as e:
        logging.error(f"Error reading OPML file: {e}")
        raise

def extract_rss_urls_from_opml(opml_content):
    """
    Extracts RSS feed URLs from OPML content.

    :param opml_content: OPML content as a string.
    :return: List of RSS feed URLs.
    """
    try:
        root = ET.fromstring(opml_content)
        rss_urls = set()  # Use a set to avoid duplicates
        for outline in root.iter('outline'):
            url = outline.attrib.get('xmlUrl')
            if url and is_valid_url(url):
                rss_urls.add(url)
        return list(rss_urls)
    except ET.ParseError as e:
        logging.error(f"Error parsing OPML content: {e}")
        raise

def write_urls_to_file(urls, output_file):
    """
    Writes URLs to a file, one per line.

    :param urls: List of URLs.
    :param output_file: Path to the output file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        with open(output_file, 'w') as f:
            for url in urls:
                f.write(url + '\n')
    except IOError as e:
        logging.error(f"Error writing to output file: {e}")
        raise

def is_valid_url(url):
    """
    Validates the URL.

    :param url: URL string.
    :return: True if URL is valid, False otherwise.
    """
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def main():
    """
    Main function to handle CLI arguments and perform OPML URL extraction.
    """
    parser = argparse.ArgumentParser(description="Extract RSS URLs from an OPML file and write them to a text file.")
    parser.add_argument('source', help="Path to the OPML file or URL of the OPML file.")
    parser.add_argument('--output', default='input/feeds.txt', help="Path to the output text file.")
    
    args = parser.parse_args()

    try:
        if os.path.isfile(args.source):
            logging.info(f"Fetching OPML from local file: {args.source}")
            opml_content = fetch_opml_from_file(args.source)
        elif args.source.startswith('http://') or args.source.startswith('https://'):
            logging.info(f"Fetching OPML from URL: {args.source}")
            opml_content = fetch_opml_from_url(args.source)
        else:
            raise ValueError("Source must be a valid file path or URL.")
        
        rss_urls = extract_rss_urls_from_opml(opml_content)
        write_urls_to_file(rss_urls, args.output)

        logging.info(f"Extracted {len(rss_urls)} RSS feed URLs to {args.output}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
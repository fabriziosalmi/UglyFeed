"""
Module for converting EPUB book chapters into an RSS feed.
"""

import os
import argparse
import requests
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from tqdm import tqdm

def download_epub(url, download_path):
    """
    Download an EPUB file from the given URL to the specified path.
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(download_path, 'wb') as file, tqdm(
        desc=download_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))
    return download_path

def extract_chapters(epub_path):
    """
    Extract chapters from the given EPUB file.
    """
    book = epub.read_epub(epub_path)
    chapters = []

    for item in tqdm(book.get_items_of_type(ebooklib.ITEM_DOCUMENT), desc="Extracting chapters"):
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text = soup.get_text(separator="\n")
            chapters.append({'title': item.get_name(), 'content': text})

    return chapters

def create_rss_feed(chapters, book_title, rss_link, output_path):
    """
    Create an RSS feed from the extracted chapters and save it to the specified path.
    """
    fg = FeedGenerator()
    fg.title(book_title)
    fg.link(href=rss_link, rel='self')
    fg.description(f"RSS feed for the book '{book_title}'")

    for chapter in tqdm(chapters, desc="Creating RSS feed"):
        fe = fg.add_entry()
        fe.title(chapter['title'])
        fe.content(chapter['content'])

    fg.rss_file(output_path)

def main():
    """
    Main function to parse arguments and generate the RSS feed.
    """
    parser = argparse.ArgumentParser(description="Convert EPUB book chapters into an RSS feed")
    parser.add_argument('--input', required=True, help="Path to the EPUB file or URL")
    parser.add_argument('--rss-link', required=True, help="Link for the RSS feed")
    parser.add_argument('--output', required=True, help="Output path and filename for the RSS feed")
    parser.add_argument('--book-title', required=True, help="Title of the book")

    args = parser.parse_args()

    epub_path = args.input
    if epub_path.startswith('http://') or epub_path.startswith('https://'):
        epub_path = download_epub(epub_path, 'temp.epub')

    try:
        chapters = extract_chapters(epub_path)
        create_rss_feed(chapters, args.book_title, args.rss_link, args.output)
        print(f"RSS feed generated and saved to {args.output}")
    except Exception as err:
        print(f"An error occurred: {err}")
    finally:
        if epub_path == 'temp.epub':
            os.remove(epub_path)

if __name__ == "__main__":
    main()

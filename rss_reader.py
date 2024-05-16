import feedparser
from typing import List, Dict
from tqdm import tqdm

def parse_rss_feed(feed_url: str) -> List[Dict]:
    feed = feedparser.parse(feed_url)
    entries = []
    for entry in feed.entries:
        parsed_entry = {
            'date': entry.get('published', ''),
            'time': entry.get('published_parsed', ''),
            'source_url': feed_url,
            'title': entry.get('title', ''),
            'content': entry.get('summary', '') or (entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '')
        }
        entries.append(parsed_entry)
    return entries

def fetch_feeds_from_file(file_path: str) -> List[Dict]:
    all_entries = []
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    for feed_url in tqdm(urls, desc="Fetching feeds"):
        try:
            entries = parse_rss_feed(feed_url)
            all_entries.extend(entries)
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")

    return all_entries


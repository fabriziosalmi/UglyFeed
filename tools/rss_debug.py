#!/usr/bin/env python3
"""
RSS Feed Debug Tool for UglyFeed

This tool helps diagnose RSS feed fetching issues that can cause 
"No Title" and empty content problems in the final XML output.

The most common issue is that RSS feeds are not being fetched properly,
leading to empty content being passed to the LLM processor.

Usage:
    python tools/rss_debug.py input/feeds.txt
    python tools/rss_debug.py --url https://example.com/feed.xml
"""

import argparse
import sys
import feedparser
import requests
from urllib.parse import urlparse
import logging
from typing import List, Dict, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate_url(url: str) -> bool:
    """Validate if URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def check_url_accessibility(url: str) -> Dict[str, any]:
    """Check if URL is accessible and returns response info."""
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'UglyFeed RSS Debug Tool 1.0'
        })
        return {
            'accessible': True,
            'status_code': response.status_code,
            'content_type': response.headers.get('content-type', 'Unknown'),
            'content_length': len(response.content),
            'encoding': response.encoding
        }
    except requests.exceptions.RequestException as e:
        return {
            'accessible': False,
            'error': str(e)
        }


def parse_rss_feed(url: str) -> Dict[str, any]:
    """Parse RSS feed and return diagnostic information."""
    try:
        logger.info(f"Parsing RSS feed: {url}")
        feed = feedparser.parse(url)
        
        # Basic feed info
        feed_info = {
            'url': url,
            'title': getattr(feed.feed, 'title', 'No feed title'),
            'description': getattr(feed.feed, 'description', 'No feed description'),
            'link': getattr(feed.feed, 'link', 'No feed link'),
            'language': getattr(feed.feed, 'language', 'No language specified'),
            'total_entries': len(feed.entries),
            'bozo': feed.bozo,  # True if feed had parsing errors
            'bozo_exception': str(feed.bozo_exception) if feed.bozo else None
        }
        
        # Sample entries analysis
        entries_info = []
        for i, entry in enumerate(feed.entries[:5]):  # Check first 5 entries
            entry_info = {
                'index': i,
                'title': getattr(entry, 'title', 'NO TITLE'),
                'title_length': len(getattr(entry, 'title', '')),
                'description': getattr(entry, 'description', 'NO DESCRIPTION'),
                'description_length': len(getattr(entry, 'description', '')),
                'link': getattr(entry, 'link', 'NO LINK'),
                'published': getattr(entry, 'published', 'NO DATE'),
                'has_content': hasattr(entry, 'content'),
                'has_summary': hasattr(entry, 'summary'),
                'available_fields': list(entry.keys())
            }
            entries_info.append(entry_info)
        
        return {
            'success': True,
            'feed_info': feed_info,
            'entries_sample': entries_info
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def diagnose_feeds_file(file_path: str) -> None:
    """Diagnose RSS feeds from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = [url.strip() for url in file.readlines() if url.strip()]
        
        logger.info(f"Found {len(urls)} URLs in {file_path}")
        
        total_articles = 0
        problematic_feeds = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*80}")
            print(f"DIAGNOSING FEED {i}/{len(urls)}: {url}")
            print(f"{'='*80}")
            
            # Validate URL format
            if not validate_url(url):
                print(f"❌ INVALID URL FORMAT: {url}")
                problematic_feeds.append({'url': url, 'issue': 'Invalid URL format'})
                continue
            
            # Check URL accessibility
            print(f"🔍 Checking URL accessibility...")
            access_info = check_url_accessibility(url)
            
            if not access_info['accessible']:
                print(f"❌ URL NOT ACCESSIBLE: {access_info['error']}")
                problematic_feeds.append({'url': url, 'issue': f"Not accessible: {access_info['error']}"})
                continue
            
            print(f"✅ URL accessible (Status: {access_info['status_code']}, Type: {access_info['content_type']})")
            
            # Parse RSS feed
            print(f"🔍 Parsing RSS feed...")
            feed_result = parse_rss_feed(url)
            
            if not feed_result['success']:
                print(f"❌ RSS PARSING FAILED: {feed_result['error']}")
                problematic_feeds.append({'url': url, 'issue': f"RSS parsing failed: {feed_result['error']}"})
                continue
            
            feed_info = feed_result['feed_info']
            entries_sample = feed_result['entries_sample']
            
            # Display feed information
            print(f"📰 FEED INFO:")
            print(f"   Title: {feed_info['title']}")
            print(f"   Description: {feed_info['description'][:100]}...")
            print(f"   Language: {feed_info['language']}")
            print(f"   Total entries: {feed_info['total_entries']}")
            
            if feed_info['bozo']:
                print(f"⚠️  FEED HAS PARSING WARNINGS: {feed_info['bozo_exception']}")
            
            # Analyze entries
            if feed_info['total_entries'] == 0:
                print(f"❌ NO ENTRIES FOUND IN FEED")
                problematic_feeds.append({'url': url, 'issue': 'No entries found'})
                continue
            
            print(f"\n📋 SAMPLE ENTRIES ANALYSIS:")
            empty_titles = 0
            empty_descriptions = 0
            
            for entry in entries_sample:
                print(f"   Entry {entry['index'] + 1}:")
                print(f"      Title: '{entry['title'][:50]}...' (Length: {entry['title_length']})")
                print(f"      Description: '{entry['description'][:50]}...' (Length: {entry['description_length']})")
                print(f"      Link: {entry['link']}")
                
                if entry['title'] == 'NO TITLE' or entry['title_length'] == 0:
                    empty_titles += 1
                    print(f"      ⚠️  EMPTY OR MISSING TITLE")
                
                if entry['description'] == 'NO DESCRIPTION' or entry['description_length'] == 0:
                    empty_descriptions += 1
                    print(f"      ⚠️  EMPTY OR MISSING DESCRIPTION")
            
            # Summary for this feed
            total_articles += feed_info['total_entries']
            
            issues = []
            if empty_titles > 0:
                issues.append(f"{empty_titles} entries with empty titles")
            if empty_descriptions > 0:
                issues.append(f"{empty_descriptions} entries with empty descriptions")
            
            if issues:
                print(f"⚠️  POTENTIAL ISSUES: {', '.join(issues)}")
                problematic_feeds.append({'url': url, 'issue': ', '.join(issues)})
            else:
                print(f"✅ FEED LOOKS GOOD")
        
        # Final summary
        print(f"\n{'='*80}")
        print(f"DIAGNOSIS SUMMARY")
        print(f"{'='*80}")
        print(f"Total feeds checked: {len(urls)}")
        print(f"Total articles found: {total_articles}")
        print(f"Problematic feeds: {len(problematic_feeds)}")
        
        if problematic_feeds:
            print(f"\n❌ ISSUES FOUND:")
            for feed in problematic_feeds:
                print(f"   • {feed['url']}: {feed['issue']}")
            
            print(f"\n🔧 RECOMMENDATIONS:")
            print(f"   1. Check if problematic URLs are valid RSS feeds")
            print(f"   2. Verify URLs are accessible from your network")
            print(f"   3. Some feeds might be temporarily down")
            print(f"   4. Consider replacing problematic feeds with alternatives")
            print(f"   5. Check if feeds require authentication or special headers")
        else:
            print(f"✅ All feeds look good!")
        
        if total_articles == 0:
            print(f"\n🚨 CRITICAL: NO ARTICLES FOUND - This will cause 'No Title' issues in UglyFeed!")
            print(f"   This explains why you're seeing empty content passed to the LLM processor.")
            
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find file {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Debug RSS feed fetching issues in UglyFeed',
        epilog="""
Examples:
  python rss_debug.py input/feeds.txt
  python rss_debug.py --url https://example.com/feed.xml
  python rss_debug.py --url https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('file', nargs='?', help='Path to feeds.txt file')
    group.add_argument('--url', help='Single RSS feed URL to test')
    
    args = parser.parse_args()
    
    print("🔍 UglyFeed RSS Debug Tool")
    print("This tool helps diagnose RSS fetching issues that cause 'No Title' problems")
    print("=" * 80)
    
    if args.url:
        # Test single URL
        print(f"Testing single URL: {args.url}")
        
        if not validate_url(args.url):
            print(f"❌ INVALID URL FORMAT")
            sys.exit(1)
        
        access_info = check_url_accessibility(args.url)
        if not access_info['accessible']:
            print(f"❌ URL NOT ACCESSIBLE: {access_info['error']}")
            sys.exit(1)
        
        feed_result = parse_rss_feed(args.url)
        if not feed_result['success']:
            print(f"❌ RSS PARSING FAILED: {feed_result['error']}")
            sys.exit(1)
        
        print("✅ URL is working correctly!")
        print(f"Feed title: {feed_result['feed_info']['title']}")
        print(f"Total entries: {feed_result['feed_info']['total_entries']}")
        
    else:
        # Test feeds file
        diagnose_feeds_file(args.file)


if __name__ == "__main__":
    main()

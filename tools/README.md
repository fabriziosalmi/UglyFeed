# UglyFeed Tools

This directory contains utility tools for debugging and maintaining UglyFeed.

## RSS Debug Tool (`rss_debug.py`)

A diagnostic tool to help troubleshoot RSS feed fetching issues that cause "No Title" and empty content problems.

### The Problem

If you're seeing output like this in your final XML:

```xml
<item>
<title>No Title</title>
<description>Forniscimi il contenuto delle fonti e sarò felice di elaborare...</description>
<pubDate>Tue, 20 Aug 2024 10:47:36 GMT</pubDate>
<guid>https://github.com/fabriziosalmi/UglyFeed/No%20Title</guid>
</item>
```

This indicates that the RSS feed fetching is failing **before** the LLM processing stage. The LLM is receiving empty content and responding appropriately.

### How to Use

1. **Debug your feeds file:**
   ```bash
   python tools/rss_debug.py input/feeds.txt
   ```

2. **Test a single RSS feed:**
   ```bash
   python tools/rss_debug.py --url https://example.com/feed.xml
   ```

3. **Test the example feeds:**
   ```bash
   python tools/rss_debug.py --url https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml
   ```

### What It Checks

- **URL Format:** Validates that URLs are properly formatted
- **Accessibility:** Checks if URLs are reachable from your network
- **RSS Format:** Verifies that feeds can be parsed as valid RSS/XML
- **Content Quality:** Analyzes if entries have titles, descriptions, and links
- **Feed Metadata:** Shows feed information and language settings

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `URL NOT ACCESSIBLE` | Network/firewall blocking | Check network connectivity, try different DNS |
| `RSS PARSING FAILED` | Invalid XML/RSS format | Verify feed URL in browser, contact feed provider |
| `NO ENTRIES FOUND` | Empty feed | Feed might be temporarily empty or outdated |
| `EMPTY OR MISSING TITLE` | Malformed feed entries | Feed provider issue, consider alternative source |
| `Invalid URL format` | Typo in feeds.txt | Fix URL formatting in your feeds file |

### Expected Output

The tool will show detailed diagnostics for each feed:

```
🔍 DIAGNOSING FEED 1/3: https://example.com/feed.xml
================================================================================
🔍 Checking URL accessibility...
✅ URL accessible (Status: 200, Type: application/rss+xml)
🔍 Parsing RSS feed...
📰 FEED INFO:
   Title: Example News Feed
   Description: Latest news from Example...
   Language: en
   Total entries: 10
📋 SAMPLE ENTRIES ANALYSIS:
   Entry 1:
      Title: 'Example News Article Title...' (Length: 45)
      Description: 'This is the article description...' (Length: 156)
      Link: https://example.com/article/1
✅ FEED LOOKS GOOD
```

### Integration with UglyFeed

The main `fetch_feeds_from_file()` function in `main.py` has been enhanced with:

- Better error handling and logging
- Validation of feed entries before processing
- Clear warnings when feeds are empty or inaccessible
- Fallback values for missing titles/descriptions
- Critical error messages that point to this debug tool

### Other Tools

- **`epub2rss.py`:** Convert EPUB books to RSS feeds
- **`opml2feeds.py`:** Extract RSS URLs from OPML files
- **`rss2teams.py`:** Send RSS updates to Microsoft Teams
- **`rss2telegram.py`:** Send RSS updates to Telegram

## Contributing

When adding new tools:
1. Add comprehensive error handling
2. Include usage examples in docstrings
3. Add entry to this README
4. Consider integration with the main UglyFeed workflow

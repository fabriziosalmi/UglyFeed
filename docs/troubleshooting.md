# Troubleshooting Guide

This guide helps you diagnose and fix common issues with UglyFeed.

## "No Title" and Empty Content Issues

### Symptoms

If you see output like this in your RSS feed:

```xml
<item>
<title>No Title</title>
<description>Forniscimi il contenuto delle fonti e sarò felice di elaborare una notizia completa e dettagliata. Sono pronto a integrare e armonizzare le informazioni, garantendo chiarezza, coerenza e precisione.</description>
<pubDate>Tue, 20 Aug 2024 10:47:36 GMT</pubDate>
<guid>https://github.com/fabriziosalmi/UglyFeed/No%20Title</guid>
</item>
```

Or in Italian:
- "Forniscimi il contenuto delle fonti..." (Provide me with the content of the sources...)
- "Mi scuso, ma non posso completare la tua richiesta. Ho bisogno di informazioni..." (I apologize, but I can't complete your request. I need information...)

### Root Cause

**This is NOT an LLM processing issue.** The problem occurs in the RSS feed fetching stage **before** content reaches the LLM. The LLM is correctly responding that it has no content to process.

### Diagnosis Steps

1. **Run the RSS Debug Tool:**
   ```bash
   python tools/rss_debug.py input/feeds.txt
   ```

2. **Check individual feeds:**
   ```bash
   python tools/rss_debug.py --url https://your-feed-url.com/feed.xml
   ```

3. **Test with known good feeds:**
   ```bash
   python tools/rss_debug.py --url https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml
   ```

### Common Causes and Solutions

#### 1. Network Connectivity Issues

**Symptoms:** `URL NOT ACCESSIBLE` errors

**Solutions:**
- Check internet connection
- Verify firewall/proxy settings
- Try different DNS servers (8.8.8.8, 1.1.1.1)
- Test URLs in a web browser

#### 2. Invalid RSS Feed URLs

**Symptoms:** `RSS PARSING FAILED` or `Invalid URL format`

**Solutions:**
- Verify URLs are complete and properly formatted
- Check for typos in `input/feeds.txt`
- Test URLs in an RSS reader or browser
- Look for redirects or authentication requirements

#### 3. Empty or Malformed Feeds

**Symptoms:** `NO ENTRIES FOUND` or `EMPTY OR MISSING TITLE`

**Solutions:**
- Contact feed provider about issues
- Find alternative sources for the same content
- Check if feeds require specific User-Agent headers
- Verify feeds aren't behind authentication

#### 4. Temporary Feed Outages

**Symptoms:** Intermittent failures, feeds that worked before

**Solutions:**
- Wait and retry later
- Check feed provider's status page
- Set up monitoring for critical feeds
- Implement retry logic with delays

### File Location Issues

#### Wrong Feeds File Path

**Check:** Verify `input/feeds.txt` exists and contains valid URLs

```bash
# Check if file exists
ls -la input/feeds.txt

# View contents
cat input/feeds.txt
```

#### Configuration Issues

**Check:** Verify `config.yaml` points to correct feeds file

```yaml
# Configuration file for UglyFeed
input_feeds_path: "input/feeds.txt"  # Make sure this path is correct
```

### Enhanced Logging

The improved `fetch_feeds_from_file()` function now provides detailed logging:

- Progress indicators for each feed
- Warnings for parsing issues
- Individual feed success/failure status
- Critical alerts when no articles are found

**Example logs:**
```
INFO - Found 3 URLs to process
INFO - Fetching feed 1/3 from https://example.com/feed.xml
WARNING - Feed https://example.com/feed.xml has parsing warnings: not well-formed
INFO - Successfully fetched 15 articles from https://example.com/feed.xml
ERROR - CRITICAL: No articles were fetched from any feeds! This will cause 'No Title' issues.
ERROR - Please check your RSS feed URLs using: python tools/rss_debug.py input/feeds.txt
```

## API and LLM Issues

### Wrong API Configuration

**Symptoms:** API errors, authentication failures

**Solutions:**
- Verify API keys are correct and active
- Check API endpoint URLs
- Ensure model names are valid
- Review API rate limits and quotas

### Token Limit Exceeded

**Symptoms:** Content truncation, incomplete responses

**Solutions:**
- Reduce content size in preprocessing
- Adjust `max_tokens` settings
- Use models with larger context windows
- Split large articles into smaller chunks

## Output and File Issues

### No JSON Files Generated

**Check:**
- Main processing completed successfully
- Output directory permissions
- Similarity threshold settings
- Grouping criteria

### XML Generation Failed

**Check:**
- JSON files exist in rewritten folder
- Configuration file is valid
- Output directory is writable
- Template files are present

## Performance Issues

### Slow Feed Fetching

**Solutions:**
- Check network latency to feed sources
- Implement parallel processing
- Cache feed responses
- Use local RSS feed aggregators

### High Memory Usage

**Solutions:**
- Process feeds in smaller batches
- Clear intermediate data
- Optimize similarity calculations
- Use memory-efficient data structures

## Testing and Validation

### Test with Sample Data

Use the provided example feeds to isolate issues:

```bash
# Copy sample feeds to your input
cp examples/uglyfeed-source-*.xml input/
echo "file://$(pwd)/input/uglyfeed-source-1.xml" > input/test-feeds.txt

# Test with sample data
python main.py --config config.yaml
```

### Validate Configuration

```bash
# Check YAML syntax
python -c "import yaml; print(yaml.safe_load(open('config.yaml')))"

# Test API connectivity
python -c "from openai import OpenAI; client = OpenAI(api_key='your-key'); print('API OK')"
```

## Getting Help

1. **Check the logs:** Look for specific error messages in console output
2. **Run diagnostics:** Use `tools/rss_debug.py` for feed issues
3. **Test components:** Isolate the problem to specific stages
4. **Review configuration:** Verify all settings are correct
5. **Check documentation:** Review the [FAQ](faq.md) and [main docs](README.md)
6. **Report issues:** Open a [GitHub issue](https://github.com/fabriziosalmi/UglyFeed/issues) with detailed logs

## Prevention

- Regularly test your RSS feeds
- Monitor feed provider status pages
- Keep backup feeds for important sources
- Implement health checks in your workflow
- Update UglyFeed regularly for bug fixes

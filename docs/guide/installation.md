# Installation & Quickstart

UglyFeed provides multiple deployment and installation options depending on your environment.

---

## Option 1: Python Package (`pip install uglypy`)

UglyFeed is published on PyPI as `uglypy`. You can install it directly into any Python 3.10+ virtual environment:

```bash
pip install uglypy
```

### Running the Web GUI:

```bash
uglypy gui
```

To bind to a specific address or disable telemetry:

```bash
uglypy gui --server.address 0.0.0.0 --browser.gatherUsageStats false
```

### Running Specific Scripts via CLI:

```bash
# Run the main aggregation pipeline
uglypy main

# Process through LLM engine
uglypy llm_processor

# Export JSON to clean RSS 2.0 XML
uglypy json2rss
```

---

## Option 2: Local Source & Streamlit

Clone the repository and run locally:

```bash
git clone https://github.com/fabriziosalmi/UglyFeed.git
cd UglyFeed

# Install requirements
pip install -r requirements.txt

# Start the Streamlit Web Application
streamlit run gui.py
```

---

## Option 3: Docker & Docker Compose

Run with pre-built Docker containers:

```bash
docker run -d \
  -p 8001:8001 \
  -p 8501:8501 \
  -v $(pwd)/input/feeds.txt:/app/input/feeds.txt \
  -v $(pwd)/config.yaml:/app/config.yaml \
  fabriziosalmi/uglyfeed:latest
```

Or with Docker Compose:

```bash
docker compose up -d
```

For complete container setup, port mappings, and volume mounts, see the [Docker Guide](/docker).

---

## Option 4: Serverless via GitHub Actions

You can use UglyFeed as a serverless application source using GitHub Actions:
- Scheduled cron triggers run the aggregation and LLM processing daily.
- The output `uglyfeed.xml` is automatically committed to your chosen repository or GitHub Pages branch.
- Sensitive API keys are protected using GitHub Actions Secrets.

See the [GitHub Actions Workflows in the Repository](https://github.com/fabriziosalmi/UglyFeed/tree/main/.github/workflows) for ready-to-use recipes for Groq, Gemini, and OpenAI.

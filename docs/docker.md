# UglyFeed (Docker)

This Docker image contains the UglyFeed application for processing RSS feeds, configuring similarity and API options, and managing JSON content.

## How to Use This Image

### Prerequisites

- **Docker**: Ensure you have Docker installed on your system. You can download and install it from [Docker's official site](https://www.docker.com/get-started).
- **Ollama** to run local models or an OpenAI/Groq API key

### Running the Container

To start the UglyFeed app, use the following `docker run` command:

```bash
docker run -p 8001:8001 -p 8501:8501 fabriziosalmi/uglyfeed:latest
```

### Accessing the Application

Once the container is running, open your web browser and navigate to `http://localhost:8501` (or the container ip address) to access the UglyFeed application.

### Volume Mounting for Persistent Storage

To persist the data in `input`, `output`, and `rewritten` directories across container runs, you can mount these directories to your local filesystem. This is useful if you want to retain the configuration files and processed data.

```bash
docker run -p 8001:8001 -p 8501:8501 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/rewritten:/app/rewritten \
  fabriziosalmi/uglyfeed:latest
```

Replace `$(pwd)` with the desired path on your host system.

### Configuration

The application allows you to configure various settings via the UglyFeed UI. These configurations are saved in the following files within the container:

- **RSS Feeds**: `input/feeds.txt`
- **Application Configuration**: `config.yaml`

### Editing Configuration Files

To pre-populate or manually edit the configuration files before running the container:

1. **Create the `input/feeds.txt` file** with your desired RSS feed URLs, one per line.
2. **Create the `config.yaml` file** with your configuration settings.

Mount these files into the container to use your custom configurations:

```bash
docker run -p 8001:8001 -p 8501:8501 \
  -v $(pwd)/input/feeds.txt:/app/input/feeds.txt \
  -v $(pwd)/config.yaml:/app/config.yaml \
  fabriziosalmi/uglyfeed:latest
```

### Executing scripts

Refer to the main documentation for the script execution process, basically just run the main, the llm_processor and the json2rss python scripts from their own dedicated pages just by clicking on the run buttons.

## Troubleshooting

- **Port Conflicts**: Ensure the ports `8001` and `8501` are not being used by another application on your host.
- **Docker Permissions**: You might need elevated permissions to run Docker commands or mount volumes, depending on your system's configuration.
- **Updating the Image**: Pull the latest image from Docker Hub to get the newest updates and features:

  ```bash
  docker pull fabriziosalmi/uglyfeed:latest
  ```

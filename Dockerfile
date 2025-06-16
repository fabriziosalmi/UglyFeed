# Multi-stage build for UglyFeed
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies including build tools for psutil
RUN apt-get update && apt-get install -y \
    git \
    curl \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base AS development
RUN pip install --no-cache-dir ipython pytest flake8
COPY . .
CMD ["streamlit", "run", "gui.py", "--server.address", "0.0.0.0", "--server.port", "8501"]

# Production stage
FROM base AS production
# Copy only necessary files
COPY *.py ./
COPY input/ ./input/
COPY moderation/ ./moderation/
COPY prompts/ ./prompts/
COPY tools/ ./tools/
COPY config.yaml ./

# Create directories for output
RUN mkdir -p output rewritten reports

# Expose ports
EXPOSE 8001 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "gui.py", "--server.address", "0.0.0.0", "--server.port", "8501"]

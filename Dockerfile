# Multi-stage build for CrewAI Document Intelligence Agent
# For local Apple Silicon builds, you can remove the explicit platform or set to arm64
FROM --platform=linux/amd64 python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY document_intelligence/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Production stage
FROM --platform=linux/amd64 python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    curl \
    poppler-utils \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user with home
RUN groupadd -r crewai && useradd -m -d /home/crewai -r -g crewai crewai

# Environment for user configs/caches
ENV HOME=/home/crewai \
    XDG_CACHE_HOME=/home/crewai/.cache \
    XDG_CONFIG_HOME=/home/crewai/.config \
    MPLCONFIGDIR=/home/crewai/.config/matplotlib

# Set working directory and copy code
WORKDIR /app
COPY document_intelligence/ /app/

# Create necessary directories and set ownership
RUN mkdir -p /app/temp /app/logs \
    "$HOME/.config/matplotlib" \
    "$HOME/.cache/fontconfig" \
    "$HOME/.embedchain" \
    && chown -R crewai:crewai /app "$HOME"

# Switch to non-root user
USER crewai

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/health || curl -f http://localhost:7860/ || exit 1

CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "7860"]
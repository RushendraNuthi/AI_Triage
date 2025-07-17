FROM python:3.9-slim

# Set metadata
LABEL maintainer="Educational Cybersecurity Project"
LABEL description="StegoMailLogger - Educational Steganography Learning Environment"
LABEL version="1.0"
LABEL purpose="educational"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    libc6-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user for security
RUN groupadd -r stegouser && \
    useradd -r -g stegouser -s /bin/bash stegouser && \
    chown -R stegouser:stegouser /app

# Switch to non-root user
USER stegouser

# Set default command
CMD ["python", "main.py", "--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Educational safety labels
LABEL educational.disclaimer="For educational use only - not for malicious purposes"
LABEL educational.environment="controlled"
LABEL educational.safety="vm-recommended"
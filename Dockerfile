FROM selenium/standalone-chrome:129.0

# Use single RUN command to reduce layers and minimize image size
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
    python3.11-full \
    python3.11-dev \
    python3.11-venv \
    python3.11-distutils \
    python3-pip \
    xvfb \
    build-essential \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/*

# Set working directory
WORKDIR /app

# Create virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3.11 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy only requirements first to leverage build cache
COPY --chown=seluser:seluser requirements.txt .

# Upgrade pip, install dependencies in one layer
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=seluser:seluser . .

# Set up X11 permissions
RUN mkdir -p /tmp/.X11-unix \
    && chmod -R 1777 /tmp/.X11-unix

# Expose ports
EXPOSE 8000 9222

# Switch to non-root user
USER seluser

# Use exec form of CMD for better signal handling
CMD ["/bin/sh", "-c", "Xvfb :99 -ac 2>/var/log/xvfb.log & uvicorn extension_api:app --host 0.0.0.0 --port 8000"]
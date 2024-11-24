FROM selenium/standalone-chrome:129.0

USER root

# Add deadsnakes PPA for Python 3.11
RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa

# install Python 3.11 and other dependencies
RUN apt-get update && apt-get install -y \
    python3.11-full python3.11-dev python3.11-venv python3.11-distutils \
    python3-pip xvfb build-essential libffi-dev \
    libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev liblcms2-dev libwebp-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# set up the working directory
WORKDIR /app

# Create and activate virtual environment with Python 3.11
ENV VIRTUAL_ENV=/app/venv
RUN python3.11 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Ensure pip is upgraded and install setuptools in the virtual environment
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies in virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# ensure correct permissions for /tmp/.X11-unix to prevent Xvfb from issuing warnings
RUN mkdir -p /tmp/.X11-unix && chmod -R 1777 /tmp/.X11-unix

# Expose ports
EXPOSE 8000
EXPOSE 9222

# Run Xvfb and the application using the virtual environment Python
CMD ["sh", "-c", "Xvfb :99 -ac 2>/var/log/xvfb.log & uvicorn extension_api:app --host 0.0.0.0 --port 8000"]
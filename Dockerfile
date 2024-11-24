FROM selenium/standalone-chrome:129.0

USER root

# install Python3, pip, venv, and Xvfb
RUN apt-get update && apt-get install -y \
    python3-full python3-pip python3-venv xvfb build-essential libffi-dev python3-dev \
    libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev liblcms2-dev libwebp-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# set up the working directory
WORKDIR /app

# Create and activate virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

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
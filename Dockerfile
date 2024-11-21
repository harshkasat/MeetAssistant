FROM selenium/standalone-chrome:129.0

USER root

# install Python3, pip, venv, and Xvfb
RUN apt-get update && apt-get install -y python3-pip python3-venv xvfb build-essential libffi-dev python3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# set Python-related environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# set up the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .


# ensure correct permissions for /tmp/.X11-unix to prevent Xvfb from issuing warnings
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# change ownership of venv to seluser and switch users
RUN chown -R seluser:seluser /opt/venv /app
USER seluser


# Expose ports
EXPOSE 8000
EXPOSE 9222

# Run Xvfb and the application
CMD ["sh", "-c", "Xvfb :99 -ac 2>/dev/null & uvicorn extension_api:app --host 0.0.0.0 --port 8000"]

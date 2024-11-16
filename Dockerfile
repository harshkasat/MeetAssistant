# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for Chrome/Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "extension_api:app", "--host", "0.0.0.0", "--port", "8000"]
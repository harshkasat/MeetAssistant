# First stage with Python and undetected-chromedriver
FROM python:3.9-slim as python-base
FROM ultrafunk/undetected-chromedriver

# Copy Python from the python image
COPY --from=python-base /usr/local/bin/python /usr/local/bin/python
COPY --from=python-base /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=python-base /usr/local/lib/libpython3.9.so.1.0 /usr/local/lib/libpython3.9.so.1.0

# Set working directory
WORKDIR /app

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
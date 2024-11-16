#!/bin/bash

echo "🚀 Starting Docker deployment..."

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t meet-assistant .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Check if a container with the same name is already running
    if [ "$(docker ps -q -f name=meet-assistant)" ]; then
        echo "🔄 Stopping existing container..."
        docker stop meet-assistant
        docker rm meet-assistant
    fi

    # Run the new container
    echo "🚀 Starting new container..."
    docker run -d --name meet-assistant -p 8000:8000 meet-assistant

    if [ $? -eq 0 ]; then
        echo "✅ Container started successfully!"
        echo "🌐 API is available at http://localhost:8000"
        echo "📚 Documentation is available at http://localhost:8000/docs"
    else
        echo "❌ Failed to start container"
    fi
else
    echo "❌ Build failed"
    exit 1
fi
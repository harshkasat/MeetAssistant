#!/bin/bash

echo "🛑 Stopping Docker container..."

if [ "$(docker ps -q -f name=fastapi-meet-bot)" ]; then
    docker stop fastapi-meet-bot
    docker rm fastapi-meet-bot
    echo "✅ Container stopped and removed successfully!"
else
    echo "ℹ️ No container was running"
fi
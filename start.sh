#!/bin/bash
echo "🚀 Starting Hardwell Underwriting Automation"
echo "Host: 0.0.0.0"
echo "Port: $PORT"
echo "Environment: Production"

# Ensure directories exist
mkdir -p static templates uploads outputs

# Start the application
exec uvicorn app_demo_enhanced:app --host 0.0.0.0 --port $PORT --access-log --log-level info

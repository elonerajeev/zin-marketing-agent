#!/bin/bash
# Start n8n with proper configuration for localhost access

# Kill any existing n8n processes
pkill -9 -f n8n 2>/dev/null
sleep 2

# Set environment variables
export N8N_SECURE_COOKIE=false
export N8N_HOST=0.0.0.0
export N8N_PORT=5678

echo "Starting n8n..."
echo "Access at: http://localhost:5678"
echo "         or http://172.29.94.205:5678"
echo ""

# Start n8n
n8n start

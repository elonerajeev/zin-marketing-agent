#!/bin/bash
# Load environment variables and run master agent

cd "$(dirname "$0")"
export $(cat .env | grep -v '^#' | xargs)
python3 master_agent.py "$@"

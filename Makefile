.PHONY: install setup start help interactive

help:
	@echo "Zin Marketing Agent - Commands:"
	@echo ""
	@echo "  make install    - Install Python dependencies"
	@echo "  make setup      - Setup environment (first time only)"
	@echo "  make start      - Start n8n server"
	@echo "  make interactive - Start interactive mode"
	@echo ""
	@echo "Usage:"
	@echo "  ./zin \"your command here\""
	@echo "  python3 interactive.py  (for chat mode)"
	@echo ""
	@echo "Examples:"
	@echo "  ./zin \"send bulk email to customers\""
	@echo "  ./zin \"generate leads for tech startups\""

install:
	@echo "Installing dependencies..."
	pip install openai anthropic requests

setup: install
	@echo "Setting up Zin Marketing Agent..."
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create it with your API keys."; \
		exit 1; \
	fi
	@chmod +x run.sh
	@chmod +x zin
	@chmod +x interactive.py
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Start n8n: make start"
	@echo "2. Use: ./zin \"your command\""
	@echo "3. Or: python3 interactive.py"

start:
	@echo "Starting n8n server..."
	@echo "Access n8n at: http://localhost:5678"
	@./start-n8n.sh

interactive:
	@python3 interactive.py

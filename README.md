# 🤖 Zin Marketing Agent

> AI-powered marketing automation agent with natural language interface, multi-step workflows, and n8n integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🌟 Features

- **Natural Language Interface** - Talk to your automations like a human
- **Multi-Step Workflows** - Chain multiple automations automatically
- **Conditional Execution** - Smart workflows that adapt based on results
- **Webhook Validation** - Ensure data integrity with response validation
- **Beautiful Terminal UI** - Color-coded output with progress tracking
- **Analytics & Tracking** - Monitor performance and success rates
- **Interactive Mode** - Chat-style interface with history
- **Environment-Based Config** - Easy dev/staging/production deployment

## 📁 Project Structure

```
zin-marketing-agent/
├── src/                    # Source code
│   ├── master_agent.py     # Main orchestrator
│   ├── styling.py          # Terminal UI utilities
│   ├── analytics.py        # Tracking & metrics
│   ├── n8n_api.py          # n8n API integration
│   └── interactive.py      # Interactive chat mode
├── config/                 # Configuration files
│   ├── automations.json    # Automation registry
│   ├── workflows.json      # Multi-step workflows
│   └── .env.example        # Environment template
├── docs/                   # Documentation
│   ├── README.md           # This file
│   ├── FEATURES.md         # Feature details
│   ├── CHANGELOG.md        # Version history
│   └── API.md              # API documentation
├── scripts/                # Utility scripts
│   ├── start-n8n.sh        # Start n8n server
│   └── run.sh              # Run helper
├── examples/               # Example workflows
├── tests/                  # Test files
├── zin                     # Main CLI entry point
├── Makefile                # Build commands
└── .gitignore              # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- n8n (self-hosted or cloud)
- OpenAI API key or Anthropic API key

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/zin-marketing-agent.git
cd zin-marketing-agent

# Install dependencies
make install
# or
pip install openai anthropic requests

# Configure environment
cp config/.env.example .env
# Edit .env and add your API keys

# Make executable
chmod +x zin
```

### Configuration

Edit `.env`:
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
LLM_PROVIDER=openai
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your-n8n-key
```

## 💡 Usage

### Single Command
```bash
./zin "send bulk email"
./zin "find leads on reddit"
```

### Multi-Step Workflows
```bash
./zin "find leads on reddit and send them emails"
```

### System Queries
```bash
./zin "how many automations do we have?"
./zin "list all automations"
```

### Interactive Mode
```bash
python3 src/interactive.py
```

## 📚 Documentation

- [Features Guide](docs/FEATURES.md) - Detailed feature documentation
- [API Reference](docs/API.md) - API and integration guide
- [Changelog](docs/CHANGELOG.md) - Version history

## 🔧 Adding New Automations

1. **Create n8n workflow** with webhook trigger
2. **Register in `config/automations.json`:**
```json
{
  "your_automation": {
    "description": "Clear description for LLM matching",
    "webhook_path": "/webhook/your-path",
    "expected_response": {
      "field": "type",
      "required_fields": ["field"]
    }
  }
}
```
3. **Test:**
```bash
./zin "your automation command"
```

## 🔗 Multi-Step Workflows

Define in `config/workflows.json`:
```json
{
  "your_workflow": {
    "description": "Workflow description",
    "steps": [
      {
        "name": "Step 1",
        "automation": "automation1",
        "description": "What it does"
      },
      {
        "name": "Step 2",
        "automation": "automation2",
        "description": "What it does",
        "condition": "previous.count > 0"
      }
    ]
  }
}
```

## 🎯 Use Cases

- **Lead Generation** - Find and qualify leads automatically
- **Email Campaigns** - Send personalized bulk emails
- **Social Media Outreach** - Automate LinkedIn, Reddit, Twitter
- **Content Marketing** - Generate and schedule content
- **Sales Pipeline** - Track deals and follow-ups
- **Competitor Monitoring** - Track competitor activity

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [n8n](https://n8n.io)
- Powered by OpenAI/Anthropic
- Inspired by the need for simple marketing automation

## 📧 Support

- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/zin-marketing-agent/issues)
- Discussions: [GitHub Discussions](https://github.com/YOUR_USERNAME/zin-marketing-agent/discussions)

---

Made with ❤️ for marketing teams and startups

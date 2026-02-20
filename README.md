# 🤖 Zin Marketing Agent

> AI-powered marketing automation with natural language control. Run n8n workflows, Python scripts, or external platforms (Make, Zapier) from your terminal.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ⚡ What Makes This Powerful

**Talk to your automations in plain English:**
```bash
./zin "generate 50 leads for software engineers in San Francisco"
./zin "schedule meeting with team for tomorrow at 2pm"
./zin "generate leads, enrich them, then send emails"
```

**No UI needed. No clicking. Just type and run.**

---

## 🎯 Key Features

### 1. **Multi-Platform Support**
Run automations on any platform:
- 🔧 **n8n** (self-hosted workflows)
- 🐍 **Python Code** (custom scripts)
- 🌐 **Make.com** (cloud automations)
- ⚡ **Zapier** (quick integrations)
- 📊 **Any webhook-based platform**

### 2. **Smart Workflow Chaining**
```bash
./zin "find leads, enrich them, then send emails"
# Automatically runs 3 automations in sequence
```

### 3. **Scheduled Automations**
```bash
./zin-schedule "generate leads" "daily at 9am"
# Runs automatically via cron
```

### 4. **Database Tracking**
Every execution saved. Track leads, emails, performance.
```bash
./zin-db stats      # Show statistics
./zin-db history    # Execution history
./zin-db leads      # All leads
```

### 5. **AI-Powered**
- Understands natural language
- Extracts parameters automatically
- Generates personalized content
- Smart suggestions

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
- n8n (optional - for n8n workflows)
- OpenAI API key

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/zin-marketing-agent.git
cd zin-marketing-agent

# Install dependencies
pip install openai anthropic requests

# Configure environment
cp config/.env.example .env
# Edit .env and add your API keys

# Make executable
chmod +x zin zin-db zin-schedule
```

### Configuration

Edit `.env`:
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
LLM_PROVIDER=openai
N8N_BASE_URL=http://localhost:5678  # Optional
```

---

## 💡 Usage

### Run Automations
```bash
./zin "send bulk email"
./zin "generate 100 leads for engineers in NYC"
./zin "schedule meeting with john@example.com for 60 minutes"
```

### Chain Workflows
```bash
./zin "find leads, enrich them, then send emails"
./zin "generate emails, then schedule follow-ups"
```

### Schedule Automations
```bash
./zin-schedule "generate leads" "daily at 9am"
./zin-schedule list
./zin-schedule remove "generate leads"
```

### Database Queries
```bash
./zin-db stats      # Show statistics
./zin-db history 20 # Last 20 executions
./zin-db leads 50   # Last 50 leads
```

### System Queries
```bash
./zin "what automations do you have?"
./zin "how many automations?"
```

---

## 🔧 Available Automations

| Automation | Platform | Category | Description |
|------------|----------|----------|-------------|
| **lead_generation** | n8n | Lead Generation | Generate leads using Apollo.io and Apify |
| **bulk_email** | n8n | Email Marketing | Send bulk emails with personalization |
| **schedule_meeting** | Python | Scheduling | Auto-schedule meetings with calendar invites |
| **enrich_leads** | Python | Lead Enrichment | Enrich with company info and scoring |
| **generate_emails** | Python | AI Content | Generate personalized cold emails with AI |

---

## 📝 Adding New Automations

### Option 1: n8n Workflow

1. Create workflow in n8n with webhook trigger
2. Add to `config/automations.json`:
```json
{
  "your_automation": {
    "description": "What it does",
    "platform": "n8n",
    "category": "Your Category",
    "webhook_path": "/webhook/your-path"
  }
}
```

### Option 2: Python Script

1. Create script in `automations/your_script.py`:
```python
def run(user_input, parameters):
    # Your code here
    return {
        "status": "success",
        "data": result
    }
```

2. Add to `config/automations.json`:
```json
{
  "your_automation": {
    "description": "What it does",
    "platform": "code",
    "category": "Your Category",
    "script_name": "your_script"
  }
}
```

### Option 3: External Platform (Make, Zapier)

1. Create automation in Make/Zapier with webhook
2. Add to `config/automations.json`:
```json
{
  "your_automation": {
    "description": "What it does",
    "platform": "make",
    "category": "Your Category",
    "webhook_url": "https://hook.make.com/your-id"
  }
}
```

---

## 🎯 Real-World Examples

### Lead Generation Pipeline
```bash
# Generate leads
./zin "generate 100 leads for SaaS founders in San Francisco"

# Enrich them
./zin "enrich leads for john@startup.io, jane@techcorp.com"

# Generate personalized emails
./zin "generate 5 cold emails for SaaS CEOs in professional tone"

# Send emails
./zin "send email to leads with subject 'Partnership Opportunity'"
```

### Meeting Automation
```bash
# Schedule meeting
./zin "schedule meeting with team@company.com for 60 minutes"

# Check database
./zin-db history
```

### Scheduled Campaigns
```bash
# Schedule daily lead generation
./zin-schedule "generate leads" "daily at 9am"

# Schedule weekly email campaign
./zin-schedule "send bulk email" "weekly"

# View all schedules
./zin-schedule list
```

---

## 📊 Database & Analytics

All executions are automatically tracked in SQLite database (`data/results.db`):

- **Executions** - Every automation run with parameters and results
- **Leads** - All generated leads (deduplicated by email)
- **Emails** - Email send records

**Query the database:**
```bash
./zin-db stats      # Overall statistics
./zin-db history 50 # Last 50 executions
./zin-db leads 100  # Last 100 leads
```

---

## 🌐 Multi-Platform Architecture

```
User Command
    ↓
Master Agent (AI)
    ↓
┌─────────┬──────────┬──────────┐
│   n8n   │  Python  │ External │
│ Webhook │  Script  │ Webhook  │
└─────────┴──────────┴──────────┘
    ↓         ↓          ↓
  Result  →  Database  →  User
```

**Benefits:**
- Use best tool for each job
- Mix platforms in one system
- Easy migration between platforms
- Cost optimization across free tiers

---

## 🔥 Advanced Features

### Workflow Chaining
Automatically detects and chains multiple automations:
```bash
./zin "generate leads, enrich them, send emails"
```

### Smart Parameter Extraction
Understands complex requests:
```bash
./zin "send email to john@example.com, jane@example.com with subject 'Meeting' and message 'See you tomorrow' as draft"
```
Extracts: `emails: [john, jane], subject: "Meeting", message: "...", draft_mode: true`

### Conditional Execution
Workflows can have conditions:
```json
{
  "steps": [
    {"automation": "generate_leads"},
    {
      "automation": "send_emails",
      "condition": "previous.count > 0"
    }
  ]
}
```

---

## 🛠️ Tech Stack

- **Python 3.8+** - Core agent
- **OpenAI GPT-4** - Natural language understanding
- **n8n** - Workflow automation (optional)
- **SQLite** - Data persistence
- **Requests** - HTTP client
- **Cron** - Scheduling

---

## 📁 Project Structure

```
zin-marketing-agent/
├── src/                    # Source code
│   ├── master_agent.py     # Main orchestrator
│   ├── code_executor.py    # Python script executor
│   ├── database.py         # SQLite database
│   ├── scheduler.py        # Cron scheduling
│   └── analytics.py        # Tracking & metrics
├── automations/            # Python automation scripts
│   ├── schedule_meeting.py
│   ├── enrich_leads.py
│   └── generate_emails.py
├── config/                 # Configuration
│   ├── automations.json    # Automation registry
│   └── .env               # API keys
├── data/                   # Database
│   └── results.db         # SQLite database
├── docs/                   # Documentation
├── zin                     # Main CLI
├── zin-db                  # Database CLI
└── zin-schedule            # Scheduling CLI
```

---

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [n8n](https://n8n.io)
- Powered by OpenAI
- Inspired by the need for simple marketing automation

---

Made with ❤️ for marketing teams and startups

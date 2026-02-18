# Master Agent System

LLM-powered router that matches natural language commands to n8n automations with advanced features.

## How It Works

```
User: "find leads on reddit and send them emails"
  ↓
Master Agent (LLM analyzes & detects multi-step)
  ↓
Step 1: n8n Webhook (reddit-leads) → Find leads
  ↓
Step 2: n8n Webhook (bulk-email) → Send emails
  ↓
Response (formatted with styling & summary)
  ↓
User: "✅ Multi-step workflow completed! 2/2 steps successful"
```

## Key Features

🚀 **Smart Automation Matching** - Natural language understanding with confidence scoring

🧠 **Parameter Extraction** - Automatically extracts emails, names, subjects from requests

🔗 **Multi-Step Workflows** - Chain multiple automations together automatically
   - Example: "find leads and email them" → runs 2 automations in sequence
   - Automatic detection of multi-step requests
   - Sequential execution with data passing

💡 **Intelligent Suggestions** - LLM-powered recommendations when no exact match

📊 **Conversation History** - Track all interactions with timestamps and results

⚡ **Interactive Mode** - Chat-style interface with persistent history

🎯 **Confidence Scoring** - See how confident the agent is about matches

🛡️ **Robust Error Handling** - Handles missing automations, failed steps, timeouts
   - Skips missing automations and continues
   - Stops on errors to prevent cascading failures
   - Clear error messages with solutions

🎨 **Beautiful Terminal Output** - Color-coded status, tables, progress bars
   - ✓ Success (green), ✗ Error (red), ⚠ Warning (yellow), ℹ Info (blue)
   - Formatted tables and boxes
   - Step-by-step progress indicators

## Key Features

🚀 **Smart Automation Matching** - Natural language understanding to match commands to workflows

🧠 **Parameter Extraction** - Automatically extracts emails, names, subjects from your requests

🔗 **Multi-Step Workflows** - Chain multiple automations together automatically
   - Example: "find leads on reddit and email them" → runs 2 automations in sequence

💡 **Intelligent Suggestions** - Get smart recommendations when no exact match is found

📊 **Conversation History** - Track all interactions with timestamps and results

⚡ **Interactive Mode** - Chat-style interface with persistent history

🎯 **Confidence Scoring** - See how confident the agent is about matches

🛡️ **Error Handling** - Clear error messages with actionable suggestions

## Quick Start

```bash
# 1. Setup (first time only)
make setup

# 2. Start n8n (separate terminal)
make start

# 3. Run commands
./zin "send bulk email"
```

**Super Simple Usage:**
```bash
./zin "your command here"
```

## Files

- `master_agent.py` - Enhanced LLM router with multi-step support
- `automations.json` - Automation registry
- `workflows.json` - Multi-step workflow definitions
- `styling.py` - Terminal styling utilities
- `.env` - API keys (OpenAI + n8n)
- `n8n_api.py` - Create workflows programmatically
- `interactive.py` - Interactive chat mode
- `zin` - Simple CLI wrapper
- `run.sh` - Helper script
- `start-n8n.sh` - n8n startup script
- `FEATURES.md` - Detailed features documentation

## Add New Automation

### 1. Create n8n workflow:
- Add **Webhook** node (POST, path: `/webhook/your-name`)
- Add your logic nodes
- Add **Respond to Webhook** node (return JSON)
- Activate workflow

### 2. Register in `automations.json`:
```json
{
  "your_automation": {
    "description": "Clear description for LLM matching",
    "webhook_path": "/webhook/your-name"
  }
}
```

Note: `webhook_path` is combined with `N8N_BASE_URL` from `.env`

### 3. Test:
```bash
./zin "your command here"
```

## Current Automations

- `bulk_email` - Send bulk emails to multiple recipients

## Configuration

Edit `.env`:
```bash
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4o-mini
LLM_PROVIDER=openai  # or anthropic
N8N_API_KEY=your-n8n-key
N8N_BASE_URL=http://localhost:5678  # Change for production
```

**Environment-based URLs:**
- Development: `N8N_BASE_URL=http://localhost:5678`
- Production: `N8N_BASE_URL=https://your-n8n-domain.com`
- No code changes needed - just update `.env`

## Architecture

**Master Agent** (`master_agent.py`):
1. `detect_multi_step()` - Detects if request needs multiple automations
2. `find_automation()` - LLM matches user input to automation
3. `extract_parameters()` - Extracts structured data from natural language
4. `execute_automation()` - Calls n8n webhook with enhanced payload
5. `execute_workflow_chain()` - Runs multiple automations sequentially
6. `analyze_result()` - LLM formats response with context
7. `suggest_automations()` - LLM-powered smart suggestions

**Styling** (`styling.py`):
- Color-coded terminal output
- Formatted tables and boxes
- Progress indicators
- Status icons

**Interactive Mode** (`interactive.py`):
- Persistent conversation
- History tracking
- Command shortcuts (history, list, clear, exit)

**n8n Workflows**:
- Handle all automation complexity
- Receive enhanced payload: `user_input`, `timestamp`, `parameters`
- Return JSON response

**Scalability**:
- Add unlimited automations (just update JSON)
- Define multi-step workflows in workflows.json
- No code changes needed
- Each workflow is independent

## n8n Workflow Template

```
┌─────────┐    ┌──────────┐    ┌──────────┐
│ Webhook │ -> │ Your     │ -> │ Respond  │
│ (POST)  │    │ Logic    │    │ to       │
│         │    │          │    │ Webhook  │
└─────────┘    └──────────┘    └──────────┘
```

**Webhook node**:
- Method: POST
- Path: unique-name
- Response Mode: "Respond to Webhook"

**Respond node**:
- Respond With: JSON
- Body: `{{ $json }}`

## Usage Examples

```bash
# Simple command
./zin "send bulk email to customers"

# With parameters (auto-extracted)
./zin "send email to john@example.com and jane@example.com with subject 'Meeting'"

# Multi-step workflow
./zin "find leads on reddit and send them emails"

# Interactive mode
python3 interactive.py
# or
make interactive

# In interactive mode:
You: send bulk email
You: history          # View past interactions
You: list            # Show available automations
You: clear           # Clear history
You: exit            # Quit

# List n8n workflows
export N8N_API_KEY="your-key"
python n8n_api.py list

# Get help
make help
```

## Troubleshooting

**"No automation found"**
- Improve description in `automations.json`
- Make it more specific for LLM matching

**"Webhook not registered"**
- Activate workflow in n8n (toggle ON)
- Check webhook path matches JSON

**"API key not found"**
```bash
export $(cat .env | grep -v '^#' | xargs)
```

## System Design

- **Minimal Core**: ~400 lines of code
- **Local**: Runs on localhost (except LLM API)
- **Scalable**: Add automations via JSON
- **Flexible**: All logic in n8n workflows
- **Intelligent**: LLM-powered matching and suggestions
- **Robust**: Comprehensive error handling
- **Beautiful**: Color-coded terminal output
- **Interactive**: Chat mode with history

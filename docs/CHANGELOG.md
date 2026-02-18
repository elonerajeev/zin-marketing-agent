# Changelog

## Version 2.0 - Advanced Features (2026-02-17)

### Added
- 🔗 **Multi-step workflow chaining** - Automatically detect and execute multiple automations in sequence
- 🧠 **Parameter extraction** - Extract emails, names, subjects from natural language
- 💡 **Intelligent suggestions** - LLM-powered recommendations when no match found
- 🎯 **Confidence scoring** - Show confidence level for automation matches
- 📊 **Conversation history** - Track all interactions with timestamps
- ⚡ **Interactive mode** - Chat-style interface with history commands
- 🎨 **Beautiful terminal output** - Color-coded status, tables, boxes, progress bars
- 🛡️ **Robust error handling** - Handle missing automations, failed steps, timeouts
- 📈 **Workflow summary** - Visual table showing success/failed/skipped steps
- 📝 **Enhanced payload** - Send timestamp and parameters to n8n workflows

### Changed
- Master agent expanded from ~100 to ~400 lines
- Improved LLM prompts for better matching
- Enhanced response formatting with context awareness
- Better error messages with actionable solutions

### Files Added
- `styling.py` - Terminal styling utilities
- `interactive.py` - Interactive chat mode
- `workflows.json` - Multi-step workflow definitions
- `FEATURES.md` - Detailed features documentation
- `CONTEXT.md` - Comprehensive project context
- `CHANGELOG.md` - This file

### Technical Improvements
- Timeout protection (30 seconds per automation)
- Exception handling for all API calls
- Data passing between workflow steps
- Progress tracking for multi-step workflows
- Summary tables with statistics

---

## Version 1.0 - Initial Release (2026-02-16)

### Added
- Basic LLM-powered automation matching
- n8n webhook integration
- Simple CLI interface (`./zin "command"`)
- OpenAI and Anthropic support
- Basic error handling
- Automation registry (automations.json)
- n8n API helper
- Environment configuration

### Files
- `master_agent.py` - Core agent (~100 lines)
- `automations.json` - Automation registry
- `.env` - Configuration
- `zin` - CLI wrapper
- `run.sh` - Helper script
- `README.md` - Documentation

# Zin Marketing Agent - Quick Reference

## ✨ New Features

### 🎨 Beautiful Terminal Output
- Color-coded status messages (✓ success, ✗ error, ⚠ warning, ℹ info)
- Progress indicators for multi-step workflows
- Formatted tables and boxes
- Clear visual hierarchy

### 🛡️ Robust Error Handling
- **Missing Automation**: Suggests alternatives and continues
- **Failed Step**: Shows error details and stops chain
- **Timeout Protection**: 30-second timeout per automation
- **Connection Errors**: Clear error messages with solutions

### 🔗 Multi-Step Workflows
- Automatic detection of multi-step requests
- Sequential execution with progress tracking
- Summary table showing success/failure/skipped
- Stops on first error to prevent cascading failures

### 💡 Smart Suggestions
- LLM-powered automation recommendations
- Explains why each suggestion is relevant
- Shows available automations when no match found

## 📊 Output Examples

### Single Automation
```
ℹ Running: bulk_email (confidence: 90%)

✓ Completed successfully!

Your bulk email has been sent...
```

### Multi-Step Workflow
```
══════════════════════════════
🔗 MULTI-STEP WORKFLOW: 2 Steps
══════════════════════════════

[1/2] Find leads on Reddit
   ℹ Running: reddit_leads
   ✓ Completed

[2/2] Send emails to leads
   ℹ Running: bulk_email
   ✓ Completed

══════════════════
📊 WORKFLOW SUMMARY
══════════════════

┌─────────────┬───────┐
│ Metric      │ Count │
├─────────────┼───────┤
│ Total Steps │ 2     │
│ Successful  │ 2     │
│ Failed      │ 0     │
│ Skipped     │ 0     │
└─────────────┴───────┘

┌───────────────────────────────────┐
│ ✓ SUCCESS                         │
├───────────────────────────────────┤
│ All steps completed successfully! │
└───────────────────────────────────┘
```

### Error Handling
```
[1/2] Find leads
   ✗ Automation "reddit_leads" not found
   ⚠ Available automations: bulk_email, simple_bulk_email
   ⚠ Skipping this step...

[2/2] Send emails
   ℹ Running: bulk_email
   ✗ Failed
   Error: Connection refused

   ⚠ Step failed. Stopping workflow chain.

┌──────────────────────────────────┐
│ ⚠ ATTENTION                      │
├──────────────────────────────────┤
│ Some steps failed. Check errors. │
└──────────────────────────────────┘
```

## 🎯 Usage Examples

### Basic Commands
```bash
./zin "send bulk email"
./zin "generate leads"
```

### Multi-Step
```bash
./zin "find leads on reddit and send them emails"
./zin "generate leads and send cold emails"
```

### With Parameters
```bash
./zin "send email to john@example.com with subject 'Meeting'"
```

### Interactive Mode
```bash
python3 interactive.py

You: send bulk email
You: history
You: list
You: exit
```

## 🔧 Error Recovery

### If Automation Not Found:
- Agent suggests similar automations
- Shows all available options
- Explains why each might be relevant

### If Step Fails:
- Shows detailed error message
- Stops workflow to prevent cascading failures
- Saves partial results in history

### If Connection Error:
- Clear error message
- Suggests checking n8n is running
- Provides troubleshooting steps

## 📈 History Tracking

All executions are tracked with:
- Input command
- Automation(s) used
- Results (success/error)
- Timestamp
- Type (single/multi-step)

View history in interactive mode:
```
You: history
```

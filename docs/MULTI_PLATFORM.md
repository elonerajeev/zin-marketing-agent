# Multi-Platform Support Guide

## 🌐 Supported Platforms

Zin Marketing Agent now supports multiple automation platforms:

- ✅ **n8n** (self-hosted)
- ✅ **Make.com** (formerly Integromat)
- ✅ **Zapier**
- ✅ **Opal** (Google)
- ✅ **Sim.ai**
- ✅ Any platform with webhook support

---

## 📝 Configuration Format

### n8n (Local)
```json
{
  "automation_name": {
    "description": "What it does",
    "platform": "n8n",
    "webhook_path": "/webhook/your-path",
    "expected_response": {
      "field": "type"
    }
  }
}
```

### External Platforms (Make, Zapier, etc.)
```json
{
  "automation_name": {
    "description": "What it does",
    "platform": "make",
    "webhook_url": "https://hook.make.com/your-webhook-id",
    "expected_response": {
      "status": "string"
    }
  }
}
```

---

## 🚀 How to Add Automations

### Example 1: Make.com

1. **Create scenario in Make.com**
2. **Add Webhook trigger**
3. **Copy webhook URL**
4. **Add to automations.json:**

```json
{
  "send_sms": {
    "description": "Send SMS to customer",
    "platform": "make",
    "webhook_url": "https://hook.make.com/abc123xyz"
  }
}
```

5. **Use it:**
```bash
./zin "send sms to customer"
```

### Example 2: Zapier

1. **Create Zap**
2. **Use "Webhooks by Zapier" trigger**
3. **Copy webhook URL**
4. **Add to automations.json:**

```json
{
  "slack_notify": {
    "description": "Send Slack notification",
    "platform": "zapier",
    "webhook_url": "https://hooks.zapier.com/hooks/catch/123/abc"
  }
}
```

5. **Use it:**
```bash
./zin "notify team on slack"
```

### Example 3: Opal (Google)

```json
{
  "update_sheets": {
    "description": "Update Google Sheets",
    "platform": "opal",
    "webhook_url": "https://opal.google/webhook/your-id"
  }
}
```

---

## 🔄 Payload Format

All platforms receive the same payload:

```json
{
  "user_input": "send email to john@example.com",
  "timestamp": "2026-02-20T12:00:00",
  "parameters": {
    "emails": ["john@example.com"],
    "subject": "Hello",
    "message": "Test message"
  }
}
```

**Your automation can use:**
- `user_input` - Original command
- `timestamp` - When triggered
- `parameters.*` - Extracted parameters

---

## 💡 Best Practices

### 1. Use Descriptive Names
```json
"send_invoice_via_stripe": {
  "description": "Send invoice to customer via Stripe",
  "platform": "make"
}
```

### 2. Document Expected Response
```json
"expected_response": {
  "status": "string",
  "invoice_id": "string",
  "amount": "number"
}
```

### 3. Test Webhooks First
```bash
curl -X POST https://your-webhook-url \
  -H "Content-Type: application/json" \
  -d '{"user_input": "test", "parameters": {}}'
```

---

## 🎯 Platform Comparison

| Platform | Hosting | Free Tier | Complexity | Best For |
|----------|---------|-----------|------------|----------|
| **n8n** | Self-hosted | Unlimited | Medium | Full control, privacy |
| **Make** | Cloud | 1,000 ops/mo | Low | Visual workflows |
| **Zapier** | Cloud | 100 tasks/mo | Low | Quick integrations |
| **Opal** | Cloud | Limited | Low | Google Workspace |
| **Sim.ai** | Cloud | Varies | Low | AI-powered |

---

## 🔧 Troubleshooting

### Webhook not responding
1. Test webhook URL directly with curl
2. Check platform is active
3. Verify webhook URL is correct

### Parameters not working
1. Check your automation reads from `parameters` object
2. Use platform's variable syntax (e.g., Make: `{{parameters.email}}`)

### Platform not supported
Add it! Just needs webhook support:
```json
{
  "your_automation": {
    "platform": "your_platform",
    "webhook_url": "https://..."
  }
}
```

---

## 📊 Example: Mixed Platform Setup

```json
{
  "lead_generation": {
    "platform": "n8n",
    "webhook_path": "/webhook/leads"
  },
  "send_email": {
    "platform": "make",
    "webhook_url": "https://hook.make.com/email123"
  },
  "notify_slack": {
    "platform": "zapier",
    "webhook_url": "https://hooks.zapier.com/slack456"
  },
  "update_crm": {
    "platform": "opal",
    "webhook_url": "https://opal.google/crm789"
  }
}
```

**Use them all:**
```bash
./zin "generate leads"           # Uses n8n
./zin "send email"                # Uses Make
./zin "notify team"               # Uses Zapier
./zin "update crm"                # Uses Opal
```

---

## 🎉 Benefits

1. **Freedom of Choice** - Use any platform you prefer
2. **Mix & Match** - Combine platforms in one system
3. **Easy Migration** - Switch platforms without changing commands
4. **Cost Optimization** - Use free tiers across platforms
5. **Best Tool for Job** - Each automation on optimal platform

---

Made with ❤️ for automation freedom

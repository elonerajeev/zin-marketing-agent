# Example: Simple Bulk Email Campaign

This example shows how to send bulk emails using natural language.

## Command

```bash
./zin "send bulk email to customers"
```

## What Happens

1. Master Agent extracts parameters (if any)
2. Matches to `bulk_email` automation
3. Triggers n8n webhook
4. n8n sends emails
5. Returns results with validation

## Expected Response

```json
{
  "Email Sent ": "Yes",
  "Status valid/Invalid": "Valid",
  "Email Address ": "customer@example.com",
  "Message Id": "abc123",
  "Sent on": "2026-02-18T10:00:00Z"
}
```

## n8n Workflow

Your n8n workflow should:
1. Receive webhook POST request
2. Extract email list from payload
3. Send emails via SMTP/SendGrid/etc
4. Return success response

## Tips

- Use personalization tokens in email templates
- Add rate limiting to avoid spam filters
- Track opens/clicks with tracking pixels
- Store results in database for analytics

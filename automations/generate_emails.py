#!/usr/bin/env python3
"""
AI-Powered Email Generator
Generates personalized cold emails using AI
"""
import os
import json

def run(user_input, parameters):
    """
    Generate personalized emails using AI
    
    Parameters:
        - recipients: number of emails to generate
        - industry: target industry
        - role: target role
        - tone: email tone (professional, casual, friendly)
        - product: product/service to pitch
    """
    recipients = parameters.get('recipients', parameters.get('count', 1))
    if not recipients or recipients == 50:  # 50 is default count, not recipients
        recipients = 2  # Default to 2 if unclear
    
    # Ensure it's an integer
    try:
        recipients = int(recipients)
    except:
        recipients = 2
    industry = parameters.get('industry', 'technology')
    role = parameters.get('role', 'decision maker')
    tone = parameters.get('tone', 'professional')
    product = parameters.get('product', 'our service')
    
    emails = []
    
    for i in range(recipients):
        email_content = generate_email(industry, role, tone, product, i+1)
        emails.append(email_content)
    
    return {
        "status": "success",
        "emails_generated": len(emails),
        "emails": emails,
        "message": f"Generated {len(emails)} personalized emails"
    }

def generate_email(industry, role, tone, product, variant=1):
    """Generate a single personalized email"""
    
    # Use OpenAI API if available
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        return generate_with_ai(industry, role, tone, product, variant)
    else:
        return generate_template(industry, role, tone, product, variant)

def generate_with_ai(industry, role, tone, product, variant):
    """Generate email using OpenAI"""
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""Write a {tone} cold email for a {role} in the {industry} industry.

Product/Service: {product}

Requirements:
- Keep it under 150 words
- Include a clear value proposition
- End with a soft call-to-action
- Make it variant #{variant} (slightly different from others)
- No placeholder names - use generic greetings

Format as JSON with: subject, body"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        
        result = response.choices[0].message.content
        
        # Parse JSON response
        import re
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            email_data = json.loads(json_match.group())
            return email_data
        
    except Exception as e:
        print(f"AI generation failed: {e}")
    
    # Fallback to template
    return generate_template(industry, role, tone, product, variant)

def generate_template(industry, role, tone, product, variant):
    """Generate email from template"""
    
    templates = {
        "professional": {
            "subject": f"Helping {industry} companies grow",
            "body": f"""Hi there,

I noticed your work in the {industry} space and wanted to reach out.

We help {role}s like you achieve better results with {product}. Our clients typically see significant improvements in their key metrics within the first month.

Would you be open to a quick 15-minute call to explore if this could work for you?

Best regards"""
        },
        "casual": {
            "subject": f"Quick question about {industry}",
            "body": f"""Hey!

Hope you're doing well. I've been following your company's growth in {industry} - impressive stuff!

We've built {product} that's been helping similar companies scale faster. Thought it might be relevant for you.

Interested in a quick chat?

Cheers"""
        },
        "friendly": {
            "subject": f"Loved your work in {industry}!",
            "body": f"""Hi!

I came across your profile and was really impressed by what you're doing in {industry}.

We've developed {product} that could complement your current efforts. Several {role}s we work with have found it valuable.

Would love to share more if you're interested!

Warm regards"""
        }
    }
    
    template = templates.get(tone, templates['professional'])
    
    # Add variation
    if variant > 1:
        template['subject'] += f" - Approach {variant}"
    
    return template

if __name__ == "__main__":
    # Test
    result = run(
        user_input="generate cold emails",
        parameters={
            "recipients": 3,
            "industry": "SaaS",
            "role": "CEO",
            "tone": "professional",
            "product": "marketing automation platform"
        }
    )
    print(json.dumps(result, indent=2))

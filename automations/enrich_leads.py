#!/usr/bin/env python3
"""
Smart Lead Enrichment Automation
Enriches lead data with company info, social profiles, and scoring
"""
import requests
import json
from datetime import datetime

def run(user_input, parameters):
    """
    Enrich lead data with additional information
    
    Parameters:
        - emails: list of email addresses to enrich
        - company: company name (optional)
        - name: person name (optional)
    """
    emails = parameters.get('emails', [])
    
    if not emails:
        return {
            "status": "error",
            "message": "No emails provided for enrichment"
        }
    
    enriched_leads = []
    
    for email in emails:
        lead_data = enrich_lead(email, parameters)
        enriched_leads.append(lead_data)
        
        # Save to database
        save_lead_to_db(lead_data)
    
    return {
        "status": "success",
        "enriched_count": len(enriched_leads),
        "leads": enriched_leads,
        "message": f"Enriched {len(enriched_leads)} leads"
    }

def enrich_lead(email, parameters):
    """Enrich a single lead with multiple data sources"""
    lead = {
        "email": email,
        "enriched_at": datetime.now().isoformat(),
        "sources": []
    }
    
    # 1. Extract domain from email
    domain = email.split('@')[1] if '@' in email else None
    lead['domain'] = domain
    
    # 2. Get company info from domain
    if domain:
        company_info = get_company_info(domain)
        lead.update(company_info)
    
    # 3. Find social profiles
    social_profiles = find_social_profiles(email, parameters.get('name'))
    lead['social_profiles'] = social_profiles
    
    # 4. Calculate lead score
    lead['score'] = calculate_lead_score(lead)
    
    # 5. Get email validation
    lead['email_valid'] = validate_email(email)
    
    return lead

def get_company_info(domain):
    """Get company information from domain"""
    # TODO: Integrate with Clearbit, Hunter.io, or similar API
    
    # Simulated company data
    company_data = {
        "company_name": domain.split('.')[0].title(),
        "company_domain": domain,
        "company_size": "Unknown",
        "industry": "Unknown",
        "location": "Unknown",
        "founded_year": None,
        "tech_stack": [],
        "social_links": {}
    }
    
    # Try to get real data (add API key in .env)
    # api_key = os.getenv('CLEARBIT_API_KEY')
    # if api_key:
    #     response = requests.get(f'https://company.clearbit.com/v2/companies/find?domain={domain}')
    #     if response.ok:
    #         company_data = response.json()
    
    return company_data

def find_social_profiles(email, name=None):
    """Find LinkedIn, Twitter, GitHub profiles"""
    profiles = {
        "linkedin": None,
        "twitter": None,
        "github": None
    }
    
    # TODO: Integrate with social profile APIs
    # For now, construct likely URLs
    username = email.split('@')[0]
    
    profiles['linkedin'] = f"https://linkedin.com/in/{username}"
    profiles['twitter'] = f"https://twitter.com/{username}"
    profiles['github'] = f"https://github.com/{username}"
    
    return profiles

def calculate_lead_score(lead):
    """Calculate lead quality score (0-100)"""
    score = 0
    
    # Email validation
    if lead.get('email_valid'):
        score += 20
    
    # Has company info
    if lead.get('company_name') and lead['company_name'] != 'Unknown':
        score += 20
    
    # Company size (prefer mid-large companies)
    company_size = lead.get('company_size', '')
    if 'enterprise' in company_size.lower():
        score += 30
    elif 'medium' in company_size.lower():
        score += 20
    elif 'small' in company_size.lower():
        score += 10
    
    # Has social profiles
    social = lead.get('social_profiles', {})
    if social.get('linkedin'):
        score += 15
    if social.get('twitter'):
        score += 10
    if social.get('github'):
        score += 5
    
    return min(score, 100)

def validate_email(email):
    """Validate email format and deliverability"""
    import re
    
    # Basic format check
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # TODO: Add real email validation API (ZeroBounce, etc.)
    return True

def save_lead_to_db(lead_data):
    """Save enriched lead to database"""
    import sys
    sys.path.insert(0, 'src')
    from database import ResultsDB
    
    db = ResultsDB()
    db.save_lead(
        name=lead_data.get('company_name', 'Unknown'),
        email=lead_data['email'],
        company=lead_data.get('company_name'),
        role=lead_data.get('role'),
        location=lead_data.get('location'),
        source='enrichment'
    )

if __name__ == "__main__":
    # Test
    result = run(
        user_input="enrich leads",
        parameters={
            "emails": ["john@techcorp.com", "jane@startup.io"]
        }
    )
    print(json.dumps(result, indent=2, default=str))

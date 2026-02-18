#!/usr/bin/env python3
"""n8n API helper - create workflows programmatically"""
import os
import requests
import json

class N8nAPI:
    def __init__(self):
        self.base_url = "http://localhost:5678/api/v1"
        self.api_key = os.getenv("N8N_API_KEY")
        self.headers = {"X-N8N-API-KEY": self.api_key}
    
    def create_workflow(self, name, webhook_path, description=""):
        """Create a simple webhook workflow"""
        workflow = {
            "name": name,
            "active": True,
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": webhook_path,
                        "responseMode": "responseNode"
                    },
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "position": [250, 300],
                    "webhookId": "",
                    "typeVersion": 1
                },
                {
                    "parameters": {
                        "respondWith": "json",
                        "responseBody": '={{ $json }}'
                    },
                    "name": "Respond",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "position": [450, 300],
                    "typeVersion": 1
                }
            ],
            "connections": {
                "Webhook": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}
            }
        }
        
        response = requests.post(
            f"{self.base_url}/workflows",
            headers=self.headers,
            json=workflow
        )
        return response.json()
    
    def list_workflows(self):
        """List all workflows"""
        response = requests.get(f"{self.base_url}/workflows", headers=self.headers)
        return response.json()

if __name__ == "__main__":
    import sys
    
    if not os.getenv("N8N_API_KEY"):
        print("❌ Set N8N_API_KEY environment variable first")
        print("Get it from: n8n Settings → API → Create API Key")
        sys.exit(1)
    
    api = N8nAPI()
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        workflows = api.list_workflows()
        print(json.dumps(workflows, indent=2))
    else:
        print("Usage:")
        print("  export N8N_API_KEY='your-key'")
        print("  python3 n8n_api.py list")

#!/usr/bin/env python3
import os
import json
import requests
import re
from datetime import datetime
from styling import *
from analytics import Analytics
from database import ResultsDB
from code_executor import CodeExecutor

class MasterAgent:
    def __init__(self):
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.n8n_base_url = os.getenv("N8N_BASE_URL", "http://localhost:5678")
        
        if self.llm_provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        else:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-5-sonnet-20241022"
        
        self.automations = self.load_automations()
        self.history = []
        self.analytics = Analytics()
        self.db = ResultsDB()
        self.code_executor = CodeExecutor()
    
    def load_automations(self):
        """Load automation registry from JSON file"""
        try:
            with open("config/automations.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def validate_response(self, automation_name, response_data):
        """Validate webhook response against expected schema"""
        automation = self.automations.get(automation_name, {})
        expected = automation.get("expected_response", {})
        
        if not expected:
            return True, None
        
        required_fields = expected.get("required_fields", [])
        
        # Check required fields
        for field in required_fields:
            if field not in response_data:
                return False, f"Missing required field: {field}"
        
        # Type validation
        for field, expected_type in expected.items():
            if field == "required_fields":
                continue
            
            if field in response_data:
                value = response_data[field]
                if expected_type == "array" and not isinstance(value, list):
                    return False, f"Field '{field}' should be array, got {type(value).__name__}"
                elif expected_type == "number" and not isinstance(value, (int, float)):
                    return False, f"Field '{field}' should be number, got {type(value).__name__}"
                elif expected_type == "string" and not isinstance(value, str):
                    return False, f"Field '{field}' should be string, got {type(value).__name__}"
        
        return True, None
    
    def evaluate_condition(self, condition, previous_result):
        """Evaluate step condition based on previous result"""
        if not condition:
            return True
        
        try:
            # Simple condition parser: "previous.field operator value"
            # Example: "previous.count > 0"
            condition = condition.replace("previous.", "previous_result.get('data', {}).get('")
            condition = condition.replace(" >", "') >")
            condition = condition.replace(" <", "') <")
            condition = condition.replace(" ==", "') ==")
            condition = condition.replace(" !=", "') !=")
            
            # Safe evaluation
            return eval(condition, {"previous_result": previous_result})
        except:
            return True  # Default to execute if condition parsing fails
    
    def extract_parameters(self, user_input):
        """Extract structured parameters from natural language"""
        prompt = f"""Extract parameters from this request as JSON:
"{user_input}"

Extract:
- emails: list of email addresses (extract ALL mentioned emails)
- recipients: number of recipients if mentioned (e.g., "3 recipients" = 3)
- subject: email subject if mentioned
- message: message content if mentioned
- draft_mode: true if user says "draft" or "don't send", false otherwise
- names: list of names if mentioned
- count: number if mentioned (default: 50)
- role: job title/role if mentioned (e.g., "engineer", "developer")
- location: city/location if mentioned (e.g., "San Francisco", "NYC")
- industry: industry/sector if mentioned (e.g., "technology", "healthcare")
- company_size: company size if mentioned (e.g., "startup", "enterprise")

Return ONLY valid JSON, no explanation."""

        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.content[0].text.strip()
        
        try:
            return json.loads(result)
        except:
            return {}
    
    def find_automation(self, user_input):
        """Use LLM to match user input to automation with confidence score"""
        automation_list = "\n".join([f"- {name}: {data['description']}" 
                                     for name, data in self.automations.items()])
        
        prompt = f"""Available automations:
{automation_list}

User request: {user_input}

Which automation best matches? Reply with ONLY the automation name from the list above.
If no good match, reply with "NONE"."""

        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            match = response.choices[0].message.content.strip()
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            match = response.content[0].text.strip()
        
        # Return match data if found
        if match in self.automations:
            return {"automation": match, "confidence": 90, "reason": "Direct match"}
        return None
    
    def execute_automation(self, automation_name, user_input, params=None):
        """Trigger automation webhook (supports multiple platforms)"""
        automation = self.automations[automation_name]
        platform = automation.get("platform", "n8n")
        
        # Build webhook URL based on platform
        if platform == "n8n":
            webhook_path = automation["webhook_path"]
            webhook_url = f"{self.n8n_base_url}{webhook_path}"
        elif platform == "code":
            # Execute Python script directly
            script_name = automation.get("script_name")
            if not script_name:
                return {"status": "error", "message": "No script_name configured"}
            
            return self.code_executor.execute_script(script_name, user_input, params or {})
        elif platform in ["make", "zapier", "opal", "sim"]:
            # External platforms use full webhook URL
            webhook_url = automation.get("webhook_url")
            if not webhook_url:
                return {"status": "error", "message": f"No webhook_url configured for {platform}"}
        else:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        
        payload = {
            "user_input": user_input,
            "timestamp": datetime.now().isoformat(),
            "parameters": params or {}
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=30)
            
            if response.ok:
                try:
                    response_data = response.json()
                    
                    # Validate response
                    is_valid, error_msg = self.validate_response(automation_name, response_data)
                    if not is_valid:
                        return {
                            "status": "error",
                            "message": f"Response validation failed: {error_msg}",
                            "data": response_data
                        }
                    
                    return {"status": "success", "data": response_data}
                except:
                    return {"status": "success", "message": response.text or "Completed"}
            else:
                return {"status": "error", "code": response.status_code, "message": response.text}
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Request timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def analyze_result(self, result, user_input):
        """Use LLM to analyze and format result with context"""
        prompt = f"""User asked: "{user_input}"

Result: {json.dumps(result, indent=2)}

Provide a clear, concise summary for the user. If there's an error, explain what went wrong and suggest a fix."""
        
        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
    
    def detect_multi_step(self, user_input):
        """Detect if user wants to chain multiple automations"""
        prompt = f"""Analyze this request: "{user_input}"

Does this require multiple steps/automations to complete?
Examples of multi-step:
- "generate leads and send them emails"
- "find prospects on reddit then email them"
- "create proposal and send bulk email"

Reply with JSON:
{{
  "is_multi_step": true/false,
  "steps": ["step1 description", "step2 description"],
  "automations": ["automation1", "automation2"]
}}

Available automations: {list(self.automations.keys())}
"""
        
        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.content[0].text.strip()
        
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"is_multi_step": False}
        except:
            return {"is_multi_step": False}
    
    def execute_workflow_chain(self, steps_data, user_input):
        """Execute multiple automations in sequence with conditional logic"""
        results = []
        steps = steps_data.get('steps', [])
        automations = steps_data.get('automations', [])
        
        print(header(f"🔗 MULTI-STEP WORKFLOW: {len(steps)} Steps"))
        
        for i, automation in enumerate(automations, 1):
            self.analytics.track_step()
            
            # Get step details
            step_desc = steps[i-1] if i <= len(steps) else f"Step {i}"
            step_name = step_desc if isinstance(step_desc, str) else step_desc.get('description', f"Step {i}")
            condition = step_desc.get('condition') if isinstance(step_desc, dict) else None
            
            print(step(i, len(steps), bold(step_name)))
            
            # Check condition
            if condition and results:
                previous_result = results[-1].get('result', {})
                should_execute = self.evaluate_condition(condition, previous_result)
                
                if not should_execute:
                    print(f"   {warning(f'Condition not met: {condition}')}")
                    print(f"   {dim('Skipping this step...')}\n")
                    
                    results.append({
                        "step": i,
                        "automation": automation,
                        "description": step_name,
                        "result": {"status": "skipped", "message": "Condition not met"},
                        "skipped": True,
                        "condition": condition
                    })
                    continue
                else:
                    print(f"   {success(f'Condition met: {condition}')}")
            
            # Check if automation exists
            if automation not in self.automations:
                err_msg = f'Automation "{automation}" not found'
                print(f"   {error(err_msg)}")
                print(f"   {warning('Available:')} {', '.join(self.automations.keys())}")
                print(f"   {warning('Skipping...')}\n")
                
                self.analytics.track_execution("multi_step", automation_name=automation, status="failed", error=err_msg)
                
                results.append({
                    "step": i,
                    "automation": automation,
                    "description": step_name,
                    "result": {"status": "error", "message": "Automation not found"},
                    "skipped": True
                })
                continue
            
            print(f"   {info(f'Running: {automation}')}")
            
            # Execute automation
            try:
                result = self.execute_automation(automation, user_input, {})
                
                if result.get("status") == "error":
                    err_detail = result.get("message", "Unknown error")
                    print(f"   {error('Failed')}")
                    print(f"   {dim(f'Error: {err_detail}')}")
                    print(f"\n   {warning('Step failed. Stopping workflow chain.')}\n")
                    
                    self.analytics.track_execution("multi_step", automation_name=automation, status="failed", error=err_detail)
                    
                    results.append({
                        "step": i,
                        "automation": automation,
                        "description": step_name,
                        "result": result,
                        "failed": True
                    })
                    break
                else:
                    print(f"   {success('Completed')}")
                    
                    # Show validation status
                    if result.get("data"):
                        print(f"   {dim('✓ Response validated')}")
                    
                    self.analytics.track_execution("multi_step", automation_name=automation, status="success")
                    
                    results.append({
                        "step": i,
                        "automation": automation,
                        "description": step_name,
                        "result": result,
                        "success": True
                    })
                    
            except Exception as e:
                print(f"   {error('Exception occurred')}")
                print(f"   {dim(str(e))}")
                
                self.analytics.track_execution("multi_step", automation_name=automation, status="failed", error=str(e))
                
                results.append({
                    "step": i,
                    "automation": automation,
                    "description": step_name,
                    "result": {"status": "error", "message": str(e)},
                    "failed": True
                })
                break
            
            print()
        
        # Summary
        self._print_workflow_summary(results)
        return results
    
    def _print_workflow_summary(self, results):
        """Print a summary of workflow execution"""
        total = len(results)
        successful = sum(1 for r in results if r.get("success"))
        failed = sum(1 for r in results if r.get("failed"))
        skipped = sum(1 for r in results if r.get("skipped"))
        
        print(header("📊 WORKFLOW SUMMARY"))
        
        summary_data = [
            ["Total Steps", str(total)],
            ["Successful", f"{Colors.BRIGHT_GREEN}{successful}{Colors.RESET}"],
            ["Failed", f"{Colors.BRIGHT_RED}{failed}{Colors.RESET}"],
            ["Skipped", f"{Colors.BRIGHT_YELLOW}{skipped}{Colors.RESET}"]
        ]
        
        print(table(["Metric", "Count"], summary_data))
        
        if failed > 0:
            print(box("⚠ ATTENTION", "Some steps failed. Check the errors above.", "warning"))
        elif skipped > 0:
            print(box("ℹ INFO", "Some steps were skipped due to missing automations.", "info"))
        else:
            print(box("✓ SUCCESS", "All steps completed successfully!", "success"))
        """Suggest relevant automations based on user input using LLM"""
        automation_list = "\n".join([f"- {name}: {data['description']}" 
                                     for name, data in self.automations.items()])
        
        prompt = f"""User wants: "{user_input}"

Available automations:
{automation_list}

Suggest 2-3 most relevant automations that could help. Explain why each would be useful.
Format: "• automation_name - reason why it's relevant"
"""
        
        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            suggestions = response.choices[0].message.content
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            suggestions = response.content[0].text
        
        return f"❓ No exact match found. Here are some suggestions:\n\n{suggestions}\n\nTry: ./zin \"<automation_name>\""
    
    def suggest_automations(self, user_input):
        """Suggest relevant automations based on user input using LLM"""
        automation_list = "\n".join([f"- {name}: {data['description']}" 
                                     for name, data in self.automations.items()])
        
        prompt = f"""User wants: "{user_input}"

Available automations:
{automation_list}

Suggest 2-3 most relevant automations that could help. Explain why each would be useful.
Format: "• automation_name - reason why it's relevant"
"""
        
        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            suggestions = response.choices[0].message.content
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            suggestions = response.content[0].text
        
        warn_msg = warning('No exact match found.')
        info_msg = info('Suggestions:')
        hint_msg = dim('Try: ./zin "<automation_name>"')
        return f"{warn_msg}\n\n{info_msg}\n{suggestions}\n\n{hint_msg}"
    
    def run(self, user_input):
        """Main execution flow with enhanced features"""
        self.analytics.start_tracking()
        
        # Handle system queries
        lower_input = user_input.lower()
        if any(word in lower_input for word in ["how many", "list", "show", "what", "all", "available", "have"]):
            if any(word in lower_input for word in ["automation", "workflow"]):
                count = len(self.automations)
                print(f"\n{info(f'Total automations: {bold(str(count))}')}\n")
                
                # Build table data with platform and category
                table_data = []
                for name, data in self.automations.items():
                    platform = data.get('platform', 'n8n')
                    category = data.get('category', 'General')
                    description = data['description'][:80] + '...' if len(data['description']) > 80 else data['description']
                    
                    table_data.append([
                        name,
                        platform.upper(),
                        category,
                        description
                    ])
                
                print(table(["Automation", "Platform", "Category", "Description"], table_data))
                self.analytics.end_tracking()
                return ""
        
        # Check for multi-step workflow
        multi_step = self.detect_multi_step(user_input)
        
        # Enhanced: Check for explicit chaining with commas or "then"
        # But exclude commas within email lists or parameters
        has_then = ' then ' in user_input.lower()
        has_comma_chain = ',' in user_input and not '@' in user_input  # Avoid email lists
        
        if has_then or has_comma_chain:
            multi_step['is_multi_step'] = True
            if not multi_step.get('automations'):
                # Parse comma-separated or "then" separated commands
                parts = re.split(r',|\s+then\s+', user_input, flags=re.IGNORECASE)
                automations = []
                for part in parts:
                    match = self.find_automation(part.strip())
                    if match:
                        automations.append(match['automation'])
                multi_step['automations'] = automations
                multi_step['steps'] = [f"Step {i+1}: {a}" for i, a in enumerate(automations)]
        
        if multi_step.get("is_multi_step") and len(multi_step.get("automations", [])) > 1:
            # Execute workflow chain
            workflow_name = multi_step.get("workflow_name", "custom_workflow")
            self.analytics.track_execution("multi_step", workflow_name=workflow_name)
            
            results = self.execute_workflow_chain(multi_step, user_input)
            
            # Store in history
            self.history.append({
                "input": user_input,
                "type": "multi_step",
                "steps": results,
                "timestamp": datetime.now().isoformat()
            })
            
            # Analyze combined results
            analysis = self.analyze_result({"multi_step_results": results}, user_input)
            
            self.analytics.end_tracking()
            self.analytics.display_analytics()
            
            return f"\n{header('📝 DETAILED RESULTS')}{analysis}"
        
        # Single automation flow
        params = self.extract_parameters(user_input)
        match_data = self.find_automation(user_input)
        
        if not match_data:
            self.analytics.end_tracking()
            return self.suggest_automations(user_input)
        
        automation = match_data["automation"]
        confidence = match_data["confidence"]
        platform = self.automations[automation].get("platform", "n8n")
        
        print(f"\n{info(f'Running: {bold(automation)}')} {dim(f'(confidence: {confidence}%)')}")
        print(f"{dim(f'Platform: {platform}')}")
        if params and any(params.values()):
            print(f"{info('Extracted parameters:')}")
            for key, value in params.items():
                if value:
                    print(f"  • {key}: {value}")
        print()
        
        result = self.execute_automation(automation, user_input, params)
        
        # Handle errors
        if result.get("status") == "error":
            error_msg = result.get("message", "Unknown error")
            print(box("❌ ERROR", error_msg, "error"))
            
            self.analytics.track_execution("single", automation_name=automation, status="failed", params=params, error=error_msg)
            
            # Store in history
            self.history.append({
                "input": user_input,
                "type": "single",
                "automation": automation,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            })
            
            self.analytics.end_tracking()
            self.analytics.display_analytics()
            
            return error(f"Automation failed: {error_msg}")
        
        self.analytics.track_execution("single", automation_name=automation, status="success", params=params)
        
        # Save to database
        import time
        exec_time = time.time() - self.analytics.start_time.timestamp() if hasattr(self.analytics, 'start_time') and self.analytics.start_time else 0
        self.db.save_execution(
            automation_name=automation,
            user_input=user_input,
            parameters=params,
            status="success",
            result=result,
            execution_time=exec_time
        )
        
        # Store in history
        self.history.append({
            "input": user_input,
            "type": "single",
            "automation": automation,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        })
        
        analysis = self.analyze_result(result, user_input)
        
        self.analytics.end_tracking()
        self.analytics.display_analytics()
        
        return f"\n{success('Completed successfully!')}\n\n{analysis}"

if __name__ == "__main__":
    import sys
    agent = MasterAgent()
    
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("Enter command: ")
    
    print(agent.run(user_input))

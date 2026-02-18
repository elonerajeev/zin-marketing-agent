#!/usr/bin/env python3
import json
from datetime import datetime
from styling import *

class Analytics:
    def __init__(self):
        self.metrics = {
            "total_executions": 0,
            "successful": 0,
            "failed": 0,
            "total_steps": 0,
            "avg_execution_time": 0,
            "automations_used": {},
            "workflows_used": {},
            "parameters_extracted": 0,
            "errors": []
        }
        self.start_time = None
        self.end_time = None
    
    def start_tracking(self):
        """Start tracking execution"""
        self.start_time = datetime.now()
    
    def end_tracking(self):
        """End tracking execution"""
        self.end_time = datetime.now()
    
    def track_execution(self, execution_type, automation_name=None, workflow_name=None, status="success", params=None, error=None):
        """Track individual execution"""
        self.metrics["total_executions"] += 1
        
        if status == "success":
            self.metrics["successful"] += 1
        else:
            self.metrics["failed"] += 1
            if error:
                self.metrics["errors"].append(error)
        
        if automation_name:
            self.metrics["automations_used"][automation_name] = self.metrics["automations_used"].get(automation_name, 0) + 1
        
        if workflow_name:
            self.metrics["workflows_used"][workflow_name] = self.metrics["workflows_used"].get(workflow_name, 0) + 1
        
        if params and any(params.values()):
            self.metrics["parameters_extracted"] += len([v for v in params.values() if v])
    
    def track_step(self):
        """Track workflow step"""
        self.metrics["total_steps"] += 1
    
    def get_execution_time(self):
        """Calculate execution time"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds()
        return 0
    
    def display_analytics(self):
        """Display comprehensive analytics"""
        exec_time = self.get_execution_time()
        
        print("\n" + "="*70)
        print(header("📊 TRACKING & ANALYTICS"))
        print("="*70 + "\n")
        
        # Execution Summary
        print(bold("⚡ EXECUTION SUMMARY"))
        summary_data = [
            ["Total Executions", str(self.metrics["total_executions"])],
            ["Successful", f"{Colors.BRIGHT_GREEN}{self.metrics['successful']}{Colors.RESET}"],
            ["Failed", f"{Colors.BRIGHT_RED}{self.metrics['failed']}{Colors.RESET}"],
            ["Total Steps", str(self.metrics["total_steps"])],
            ["Execution Time", f"{exec_time:.2f}s"]
        ]
        print(table(["Metric", "Value"], summary_data))
        
        # Success Rate
        if self.metrics["total_executions"] > 0:
            success_rate = (self.metrics["successful"] / self.metrics["total_executions"]) * 100
            print(f"\n{bold('Success Rate:')} {success_rate:.1f}%")
            print(progress_bar(success_rate, 100, width=50))
        
        # Automations Used
        if self.metrics["automations_used"]:
            print(f"\n{bold('🔧 AUTOMATIONS USED')}")
            auto_data = [[name, str(count)] for name, count in sorted(self.metrics["automations_used"].items(), key=lambda x: x[1], reverse=True)]
            print(table(["Automation", "Count"], auto_data))
        
        # Workflows Used
        if self.metrics["workflows_used"]:
            print(f"\n{bold('🔗 WORKFLOWS USED')}")
            workflow_data = [[name, str(count)] for name, count in sorted(self.metrics["workflows_used"].items(), key=lambda x: x[1], reverse=True)]
            print(table(["Workflow", "Count"], workflow_data))
        
        # Parameters Extracted
        if self.metrics["parameters_extracted"] > 0:
            print(f"\n{bold('📝 PARAMETERS EXTRACTED:')} {self.metrics['parameters_extracted']}")
        
        # Errors
        if self.metrics["errors"]:
            print(f"\n{bold('❌ ERRORS ENCOUNTERED:')}")
            for i, error in enumerate(self.metrics["errors"][:5], 1):
                print(f"  {i}. {dim(error)}")
        
        # Performance Insights
        print(f"\n{bold('💡 INSIGHTS')}")
        insights = []
        
        if self.metrics["failed"] > 0:
            insights.append(f"⚠ {self.metrics['failed']} execution(s) failed - review error logs")
        
        if exec_time > 30:
            insights.append(f"⏱ Execution took {exec_time:.1f}s - consider optimizing workflows")
        
        if self.metrics["total_steps"] > 5:
            insights.append(f"🔗 Complex workflow with {self.metrics['total_steps']} steps executed")
        
        if not insights:
            insights.append("✓ All executions completed successfully")
        
        for insight in insights:
            print(f"  • {insight}")
        
        print("\n" + "="*70 + "\n")

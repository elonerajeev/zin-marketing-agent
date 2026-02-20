#!/usr/bin/env python3
"""
CLI commands for database operations
"""
import sys
sys.path.insert(0, 'src')

from database import ResultsDB
from styling import *

def show_stats():
    """Show database statistics"""
    db = ResultsDB()
    stats = db.get_stats()
    
    print(header("📊 DATABASE STATISTICS"))
    print(table(
        ["Metric", "Count"],
        [
            ["Total Executions", str(stats['total_executions'])],
            ["Successful Executions", str(stats['successful_executions'])],
            ["Total Leads", str(stats['total_leads'])],
            ["Total Emails Sent", str(stats['total_emails'])]
        ]
    ))

def show_leads(limit=20):
    """Show recent leads"""
    db = ResultsDB()
    leads = db.get_leads(limit=limit)
    
    print(header(f"📋 RECENT LEADS (Last {limit})"))
    
    if not leads:
        print(warning("No leads found in database"))
        return
    
    data = []
    for lead in leads:
        data.append([
            lead[1][:30],  # name
            lead[2],       # email
            lead[3] or "-",  # company
            lead[4] or "-",  # role
            lead[6] or "-"   # source
        ])
    
    print(table(
        ["Name", "Email", "Company", "Role", "Source"],
        data
    ))

def show_history(limit=10):
    """Show execution history"""
    db = ResultsDB()
    executions = db.get_recent_executions(limit=limit)
    
    print(header(f"📜 EXECUTION HISTORY (Last {limit})"))
    
    if not executions:
        print(warning("No executions found"))
        return
    
    data = []
    for exec in executions:
        status_icon = success("✓") if exec[1] == "success" else error("✗")
        data.append([
            exec[0],  # automation
            status_icon,
            exec[2],  # timestamp
            f"{exec[3]:.2f}s"  # execution time
        ])
    
    print(table(
        ["Automation", "Status", "Timestamp", "Time"],
        data
    ))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/db_cli.py [stats|leads|history]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "stats":
        show_stats()
    elif command == "leads":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        show_leads(limit)
    elif command == "history":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        show_history(limit)
    else:
        print(error(f"Unknown command: {command}"))
        print("Available: stats, leads, history")

#!/usr/bin/env python3
"""
Scheduling module for Zin automations
"""
import os
import re
from pathlib import Path

class Scheduler:
    def __init__(self):
        self.cron_file = Path.home() / ".zin_cron"
    
    def parse_schedule(self, schedule_text):
        """Parse natural language schedule to cron format"""
        schedule_text = schedule_text.lower()
        
        # Daily patterns
        if "daily" in schedule_text or "every day" in schedule_text:
            # Extract time
            time_match = re.search(r'(\d{1,2})\s*(am|pm)', schedule_text)
            if time_match:
                hour = int(time_match.group(1))
                period = time_match.group(2)
                
                if period == "pm" and hour != 12:
                    hour += 12
                elif period == "am" and hour == 12:
                    hour = 0
                
                return f"0 {hour} * * *"  # Every day at specified hour
        
        # Hourly patterns
        if "hourly" in schedule_text or "every hour" in schedule_text:
            return "0 * * * *"
        
        # Weekly patterns
        if "weekly" in schedule_text:
            return "0 9 * * 1"  # Every Monday at 9 AM
        
        # Default: daily at 9 AM
        return "0 9 * * *"
    
    def add_schedule(self, command, schedule_text):
        """Add a scheduled automation"""
        cron_time = self.parse_schedule(schedule_text)
        
        # Get absolute path to zin script
        zin_path = os.path.abspath("./zin")
        
        # Create cron entry
        cron_entry = f'{cron_time} cd {os.getcwd()} && {zin_path} "{command}" >> logs/cron.log 2>&1\n'
        
        # Read existing crontab
        existing_cron = os.popen("crontab -l 2>/dev/null").read()
        
        # Check if already exists
        if command in existing_cron:
            return False, "Schedule already exists for this command"
        
        # Add new entry
        new_cron = existing_cron + cron_entry
        
        # Write to temp file
        with open("/tmp/zin_crontab", "w") as f:
            f.write(new_cron)
        
        # Install crontab
        os.system("crontab /tmp/zin_crontab")
        
        # Save to our tracking file
        with open(self.cron_file, "a") as f:
            f.write(f"{cron_time}|{command}|{schedule_text}\n")
        
        return True, f"Scheduled: {command} ({cron_time})"
    
    def list_schedules(self):
        """List all scheduled automations"""
        if not self.cron_file.exists():
            return []
        
        schedules = []
        with open(self.cron_file, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        schedules.append({
                            "cron": parts[0],
                            "command": parts[1],
                            "description": parts[2]
                        })
        return schedules
    
    def remove_schedule(self, command):
        """Remove a scheduled automation"""
        # Read existing crontab
        existing_cron = os.popen("crontab -l 2>/dev/null").read()
        
        # Remove matching lines
        new_cron = "\n".join([
            line for line in existing_cron.split("\n")
            if command not in line
        ])
        
        # Write back
        with open("/tmp/zin_crontab", "w") as f:
            f.write(new_cron)
        
        os.system("crontab /tmp/zin_crontab")
        
        # Update tracking file
        if self.cron_file.exists():
            schedules = self.list_schedules()
            with open(self.cron_file, "w") as f:
                for sched in schedules:
                    if sched["command"] != command:
                        f.write(f"{sched['cron']}|{sched['command']}|{sched['description']}\n")
        
        return True, "Schedule removed"

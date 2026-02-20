#!/usr/bin/env python3
"""
Meeting Scheduler Automation
Finds available time slots and schedules meetings
"""
from datetime import datetime, timedelta
import json

def run(user_input, parameters):
    """
    Schedule a meeting with automatic time slot detection
    
    Parameters:
        - attendees: list of email addresses
        - duration: meeting duration in minutes (default: 30)
        - date: preferred date (default: tomorrow)
        - title: meeting title
        - description: meeting description
    """
    attendees = parameters.get('emails', [])
    duration = parameters.get('duration', 30)
    title = parameters.get('subject', 'Team Meeting')
    description = parameters.get('message', '')
    
    # Find available slots (next 7 days, 9 AM - 5 PM)
    available_slots = find_available_slots(duration)
    
    if not available_slots:
        return {
            "status": "error",
            "message": "No available time slots found"
        }
    
    # Pick the first available slot
    best_slot = available_slots[0]
    
    # Create meeting
    meeting = {
        "title": title,
        "description": description,
        "start_time": best_slot['start'].isoformat(),
        "end_time": best_slot['end'].isoformat(),
        "attendees": attendees,
        "duration_minutes": duration,
        "meeting_link": generate_meeting_link(),
        "calendar_invite": create_calendar_invite(best_slot, title, attendees)
    }
    
    # Save to database (optional)
    save_meeting(meeting)
    
    return {
        "status": "success",
        "meeting": meeting,
        "available_slots": len(available_slots),
        "message": f"Meeting scheduled for {best_slot['start'].strftime('%Y-%m-%d %H:%M')}"
    }

def find_available_slots(duration_minutes):
    """Find available time slots in the next 7 days"""
    slots = []
    now = datetime.now()
    
    for day in range(1, 8):  # Next 7 days
        date = now + timedelta(days=day)
        
        # Skip weekends
        if date.weekday() >= 5:
            continue
        
        # Check 9 AM to 5 PM
        for hour in range(9, 17):
            start = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end = start + timedelta(minutes=duration_minutes)
            
            # Check if slot is available (simplified - add real calendar check)
            if is_slot_available(start, end):
                slots.append({
                    'start': start,
                    'end': end,
                    'duration': duration_minutes
                })
    
    return slots

def is_slot_available(start, end):
    """Check if time slot is available (add real calendar integration)"""
    # TODO: Integrate with Google Calendar API or Outlook
    # For now, return True for all slots
    return True

def generate_meeting_link():
    """Generate video meeting link"""
    # TODO: Integrate with Zoom/Google Meet/Teams API
    import random
    meeting_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return f"https://meet.example.com/{meeting_id}"

def create_calendar_invite(slot, title, attendees):
    """Create iCal format calendar invite"""
    ical = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Zin Agent//Meeting Scheduler//EN
BEGIN:VEVENT
UID:{slot['start'].timestamp()}@zin-agent
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{slot['start'].strftime('%Y%m%dT%H%M%S')}
DTEND:{slot['end'].strftime('%Y%m%dT%H%M%S')}
SUMMARY:{title}
ATTENDEE:{''.join([f'mailto:{email}' for email in attendees])}
END:VEVENT
END:VCALENDAR"""
    return ical

def save_meeting(meeting):
    """Save meeting to database"""
    import sys
    sys.path.insert(0, 'src')
    from database import ResultsDB
    
    db = ResultsDB()
    # Save as execution record
    db.save_execution(
        automation_name="schedule_meeting",
        user_input=meeting['title'],
        parameters=meeting,
        status="success",
        result=meeting,
        execution_time=0
    )

if __name__ == "__main__":
    # Test
    result = run(
        user_input="schedule meeting with team",
        parameters={
            "emails": ["john@example.com", "jane@example.com"],
            "subject": "Sprint Planning",
            "message": "Discuss next sprint goals",
            "duration": 60
        }
    )
    print(json.dumps(result, indent=2, default=str))

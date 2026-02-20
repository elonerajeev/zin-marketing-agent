#!/usr/bin/env python3
"""
Database module for storing automation results
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class ResultsDB:
    def __init__(self, db_path="data/results.db"):
        self.db_path = db_path
        Path("data").mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Executions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                automation_name TEXT NOT NULL,
                user_input TEXT,
                parameters TEXT,
                status TEXT,
                result TEXT,
                error TEXT,
                execution_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Leads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                company TEXT,
                role TEXT,
                location TEXT,
                source TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Emails table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                subject TEXT,
                status TEXT,
                sent_at TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_execution(self, automation_name, user_input, parameters, status, result, error=None, execution_time=0):
        """Save automation execution"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO executions (automation_name, user_input, parameters, status, result, error, execution_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            automation_name,
            user_input,
            json.dumps(parameters),
            status,
            json.dumps(result),
            error,
            execution_time
        ))
        
        conn.commit()
        execution_id = cursor.lastrowid
        conn.close()
        return execution_id
    
    def save_lead(self, name, email, company=None, role=None, location=None, source=None):
        """Save lead (ignore duplicates)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO leads (name, email, company, role, location, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, company, role, location, source))
            conn.commit()
            lead_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Email already exists
            cursor.execute("SELECT id FROM leads WHERE email = ?", (email,))
            lead_id = cursor.fetchone()[0]
        
        conn.close()
        return lead_id
    
    def save_email(self, lead_id, subject, status='sent'):
        """Save email record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO emails (lead_id, subject, status, sent_at)
            VALUES (?, ?, ?, ?)
        """, (lead_id, subject, status, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_recent_executions(self, limit=10):
        """Get recent executions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT automation_name, status, created_at, execution_time
            FROM executions
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_leads(self, status=None, limit=100):
        """Get leads"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT id, name, email, company, role, location, source, created_at
                FROM leads
                WHERE status = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (status, limit))
        else:
            cursor.execute("""
                SELECT id, name, email, company, role, location, source, created_at
                FROM leads
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM executions")
        total_executions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM executions WHERE status = 'success'")
        successful_executions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM emails")
        total_emails = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "total_leads": total_leads,
            "total_emails": total_emails
        }

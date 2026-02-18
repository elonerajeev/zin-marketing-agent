#!/usr/bin/env python3
"""Interactive mode for Zin Marketing Agent with conversation history"""
import os
import sys
import json
from master_agent import MasterAgent

def print_banner():
    print("\n" + "="*60)
    print("🤖 ZIN MARKETING AGENT - Interactive Mode")
    print("="*60)
    print("Commands:")
    print("  - Type your request naturally")
    print("  - 'history' - Show conversation history")
    print("  - 'list' or 'show automations' - List available automations")
    print("  - 'clear' - Clear history")
    print("  - 'exit' or 'quit' - Exit")
    print("="*60 + "\n")

def main():
    # Load environment
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    
    agent = MasterAgent()
    print_banner()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                
                # Display session analytics
                if agent.history:
                    from analytics import Analytics
                    agent.analytics.display_analytics()
                
                break
            
            if user_input.lower() == 'history':
                if agent.history:
                    print("\n📜 Conversation History:")
                    for i, item in enumerate(agent.history, 1):
                        print(f"\n{i}. {item['timestamp']}")
                        print(f"   Input: {item['input']}")
                        print(f"   Automation: {item['automation']}")
                        print(f"   Status: {item['result'].get('status', 'unknown')}")
                else:
                    print("\n📜 No history yet")
                continue
            
            if user_input.lower() == 'list':
                print("\n📋 Available Automations:")
                for name, data in agent.automations.items():
                    print(f"  • {name}: {data['description']}")
                continue
            
            if user_input.lower() == 'clear':
                agent.history = []
                from analytics import Analytics
                agent.analytics = Analytics()
                print("\n🗑️  History and analytics cleared")
                continue
            
            # Process request
            print()
            result = agent.run(user_input)
            print(result)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()

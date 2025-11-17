"""
Keep MongoDB Alive
Periodically ping MongoDB to prevent auto-pause (free tier)
"""

import time
from pymongo import MongoClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import MONGO_URI, DB_NAME
from datetime import datetime

def ping_mongodb():
    """Ping MongoDB to keep connection alive"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        db.command('ping')
        client.close()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ MongoDB ping successful")
        return True
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Ping failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting MongoDB keep-alive script...")
    print("   This will ping MongoDB every 30 minutes")
    print("   Press Ctrl+C to stop\n")
    
    try:
        while True:
            ping_mongodb()
            time.sleep(1800)  # 30 minutes
    except KeyboardInterrupt:
        print("\n\n👋 Stopping keep-alive script...")


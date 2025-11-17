"""
Test MongoDB Connection
Diagnostic script to test MongoDB Atlas connection
"""

from pymongo import MongoClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import MONGO_URI, DB_NAME

print("="*60)
print("MongoDB Connection Test")
print("="*60)

try:
    print(f"\n📡 Connecting to MongoDB...")
    print(f"Database: {DB_NAME}")
    
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    
    # Test connection
    db.command('ping')
    print("✅ Connection successful!")
    
    # Get database info
    collections = db.list_collection_names()
    print(f"\n📊 Collections: {', '.join(collections) if collections else 'None'}")
    
    # Count documents
    for collection_name in ['animals', 'adopters', 'adoptions', 'medical_records', 'volunteers']:
        count = db[collection_name].count_documents({})
        print(f"   - {collection_name}: {count} documents")
    
    client.close()
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("\n💡 Troubleshooting tips:")
    print("   1. Check your MONGO_URI in .env file")
    print("   2. Ensure MongoDB Atlas cluster is running (not paused)")
    print("   3. Verify network access in MongoDB Atlas")
    print("   4. Check if your IP is whitelisted")
    sys.exit(1)


"""
Database Connection Module
Handles MongoDB connection and database access
"""

from pymongo import MongoClient
from pymongo.database import Database
from backend.config import MONGO_URI, DB_NAME
from typing import Optional

_client: Optional[MongoClient] = None
_database: Optional[Database] = None


def get_database() -> Optional[Database]:
    """Get MongoDB database instance"""
    global _client, _database
    
    if _database is not None:
        return _database
    
    try:
        _client = MongoClient(MONGO_URI)
        _database = _client[DB_NAME]
        # Test connection
        _database.command('ping')
        return _database
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None


def close_database():
    """Close MongoDB connection"""
    global _client, _database
    if _client:
        _client.close()
        _client = None
        _database = None


def serialize_doc(doc: dict) -> dict:
    """Convert ObjectId to string for JSON serialization and prepare for Pydantic"""
    if doc and '_id' in doc:
        # Keep _id for Pydantic models that use alias
        doc['_id'] = str(doc['_id'])
    return doc


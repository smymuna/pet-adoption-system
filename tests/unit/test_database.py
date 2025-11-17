"""
Unit Tests - Database Connection and Utilities
"""

import pytest
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

from backend.database.connection import get_database, serialize_doc, close_database
from backend.config import MONGO_URI, DB_NAME


class TestDatabaseConnection:
    """Test database connection functionality"""
    
    def test_get_database_connection(self):
        """Test that database connection works"""
        db = get_database()
        assert db is not None
        assert db.name == DB_NAME
    
    def test_database_ping(self):
        """Test database ping command"""
        db = get_database()
        result = db.command('ping')
        assert result['ok'] == 1.0
    
    def test_database_close(self):
        """Test database connection closure"""
        db = get_database()
        assert db is not None
        close_database()
        # Connection should still work after close (singleton pattern)
        db2 = get_database()
        assert db2 is not None


class TestSerializeDoc:
    """Test document serialization"""
    
    def test_serialize_doc_with_objectid(self):
        """Test serializing document with ObjectId"""
        doc = {
            '_id': ObjectId(),
            'name': 'Test',
            'value': 123
        }
        serialized = serialize_doc(doc)
        assert isinstance(serialized['_id'], str)
        assert serialized['name'] == 'Test'
        assert serialized['value'] == 123
    
    def test_serialize_doc_without_id(self):
        """Test serializing document without _id"""
        doc = {'name': 'Test', 'value': 123}
        serialized = serialize_doc(doc)
        assert serialized == doc
    
    def test_serialize_empty_doc(self):
        """Test serializing empty document"""
        doc = {}
        serialized = serialize_doc(doc)
        assert serialized == {}
    
    def test_serialize_none_doc(self):
        """Test serializing None document"""
        serialized = serialize_doc(None)
        assert serialized is None
    
    def test_serialize_doc_preserves_other_fields(self):
        """Test that serialization preserves all other fields"""
        doc = {
            '_id': ObjectId(),
            'name': 'Test',
            'age': 5,
            'nested': {'key': 'value'},
            'list': [1, 2, 3]
        }
        serialized = serialize_doc(doc)
        assert isinstance(serialized['_id'], str)
        assert serialized['name'] == 'Test'
        assert serialized['age'] == 5
        assert serialized['nested'] == {'key': 'value'}
        assert serialized['list'] == [1, 2, 3]


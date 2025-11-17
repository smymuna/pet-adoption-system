"""
Pytest Configuration and Fixtures
Shared test fixtures and configuration
"""

import pytest
import os
import sys
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import MONGO_URI, DB_NAME
from backend.database.connection import get_database, close_database, serialize_doc


@pytest.fixture(scope="session")
def test_db():
    """Create a test database connection"""
    client = MongoClient(MONGO_URI)
    test_db_name = f"{DB_NAME}_test"
    db = client[test_db_name]
    
    # Clean up test database before tests
    client.drop_database(test_db_name)
    
    yield db
    
    # Clean up after tests
    client.drop_database(test_db_name)
    client.close()


@pytest.fixture(scope="function")
def clean_db(test_db):
    """Clean database before each test"""
    collections = ['animals', 'adopters', 'adoptions', 'medical_records', 'volunteers']
    for collection in collections:
        test_db[collection].delete_many({})
    yield test_db


@pytest.fixture
def sample_animal(test_db):
    """Create a sample animal for testing"""
    animal = {
        'name': 'Test Dog',
        'species': 'Dog',
        'age': 3,
        'gender': 'Male',
        'status': 'Available'
    }
    result = test_db.animals.insert_one(animal)
    animal['_id'] = result.inserted_id
    return serialize_doc(animal)


@pytest.fixture
def sample_adopter(test_db):
    """Create a sample adopter for testing"""
    adopter = {
        'name': 'John Test',
        'phone': '555-1234',
        'email': 'john@test.com',
        'address': '123 Test St'
    }
    result = test_db.adopters.insert_one(adopter)
    adopter['_id'] = result.inserted_id
    return serialize_doc(adopter)


@pytest.fixture
def sample_adoption(test_db, sample_animal, sample_adopter):
    """Create a sample adoption for testing"""
    adoption = {
        'animal_id': str(sample_animal['_id']),
        'adopter_id': str(sample_adopter['_id']),
        'adoption_date': datetime.now().strftime('%Y-%m-%d'),
        'notes': 'Test adoption'
    }
    result = test_db.adoptions.insert_one(adoption)
    adoption['_id'] = str(result.inserted_id)
    return adoption


@pytest.fixture
def sample_medical_record(test_db, sample_animal):
    """Create a sample medical record for testing"""
    record = {
        'animal_id': str(sample_animal['_id']),
        'vet_name': 'Dr. Test',
        'visit_date': datetime.now().strftime('%Y-%m-%d'),
        'diagnosis': 'Healthy',
        'treatment': 'Vaccination',
        'notes': 'Routine checkup'
    }
    result = test_db.medical_records.insert_one(record)
    record['_id'] = str(result.inserted_id)
    return record


@pytest.fixture
def sample_volunteer(test_db):
    """Create a sample volunteer for testing"""
    volunteer = {
        'name': 'Jane Volunteer',
        'phone': '555-5678',
        'email': 'jane@test.com',
        'skills': 'Animal Care',
        'availability': 'Weekends'
    }
    result = test_db.volunteers.insert_one(volunteer)
    volunteer['_id'] = result.inserted_id
    return serialize_doc(volunteer)


"""
Add Sample Data
Populate the database with sample data for testing
"""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import MONGO_URI, DB_NAME

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ Connection error: {e}")
    sys.exit(1)

# Sample data
animals_data = [
    {"name": "Buddy", "species": "Dog", "age": 2, "gender": "Male", "status": "Available"},
    {"name": "Luna", "species": "Cat", "age": 1, "gender": "Female", "status": "Available"},
    {"name": "Max", "species": "Dog", "age": 3, "gender": "Male", "status": "Adopted"},
    {"name": "Whiskers", "species": "Cat", "age": 2, "gender": "Male", "status": "Available"},
    {"name": "Bella", "species": "Dog", "age": 4, "gender": "Female", "status": "Available"},
]

adopters_data = [
    {"name": "John Doe", "phone": "555-0101", "email": "john@example.com", "address": "123 Main St"},
    {"name": "Jane Smith", "phone": "555-0102", "email": "jane@example.com", "address": "456 Oak Ave"},
    {"name": "Bob Johnson", "phone": "555-0103", "email": "bob@example.com", "address": "789 Pine Rd"},
]

volunteers_data = [
    {"name": "Alice Brown", "phone": "555-0201", "email": "alice@example.com", "skills": "Animal Care", "availability": "Weekends"},
    {"name": "Charlie Wilson", "phone": "555-0202", "email": "charlie@example.com", "skills": "Training", "availability": "Weekdays"},
]

print("\n📝 Adding sample data...")

# Clear existing data (optional - comment out if you want to keep existing data)
# db.animals.delete_many({})
# db.adopters.delete_many({})
# db.adoptions.delete_many({})
# db.medical_records.delete_many({})
# db.volunteers.delete_many({})

# Insert animals
animals_result = db.animals.insert_many(animals_data)
print(f"✅ Added {len(animals_result.inserted_ids)} animals")

# Insert adopters
adopters_result = db.adopters.insert_many(adopters_data)
print(f"✅ Added {len(adopters_result.inserted_ids)} adopters")

# Insert adoptions (if we have adopted animals)
adopted_animal = db.animals.find_one({"name": "Max"})
if adopted_animal:
    adopter = db.adopters.find_one({"name": "John Doe"})
    if adopter:
        adoption_data = {
            "animal_id": str(adopted_animal["_id"]),
            "adopter_id": str(adopter["_id"]),
            "adoption_date": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            "notes": "Great match!"
        }
        db.adoptions.insert_one(adoption_data)
        print("✅ Added 1 adoption")

# Insert medical records
animal = db.animals.find_one({"name": "Luna"})
if animal:
    medical_data = {
        "animal_id": str(animal["_id"]),
        "vet_name": "Dr. Smith",
        "visit_date": datetime.now().strftime('%Y-%m-%d'),
        "diagnosis": "Routine checkup",
        "treatment": "Vaccination",
        "notes": "Healthy"
    }
    db.medical_records.insert_one(medical_data)
    print("✅ Added 1 medical record")

# Insert volunteers
volunteers_result = db.volunteers.insert_many(volunteers_data)
print(f"✅ Added {len(volunteers_result.inserted_ids)} volunteers")

print("\n✅ Sample data added successfully!")
client.close()


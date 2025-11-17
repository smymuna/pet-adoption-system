"""
Integration Tests - Search Operations
"""

import pytest
from bson import ObjectId
from datetime import datetime


class TestSearchOperations:
    """Test search functionality"""
    
    def test_search_animals_by_adopter(self, clean_db, sample_adopter):
        """Test finding all animals adopted by a specific adopter"""
        # Create multiple animals
        animals = [
            {'name': 'Dog1', 'species': 'Dog', 'age': 1, 'gender': 'Male', 'status': 'Available'},
            {'name': 'Dog2', 'species': 'Dog', 'age': 2, 'gender': 'Female', 'status': 'Available'},
            {'name': 'Cat1', 'species': 'Cat', 'age': 3, 'gender': 'Male', 'status': 'Available'}
        ]
        animal_results = clean_db.animals.insert_many(animals)
        
        # Create adoptions for first two animals
        for animal_id in animal_results.inserted_ids[:2]:
            adoption = {
                'animal_id': str(animal_id),
                'adopter_id': str(sample_adopter['_id']),
                'adoption_date': datetime.now().strftime('%Y-%m-%d')
            }
            clean_db.adoptions.insert_one(adoption)
        
        # Search for animals by adopter
        adoptions = list(clean_db.adoptions.find({'adopter_id': str(sample_adopter['_id'])}))
        assert len(adoptions) == 2
        
        # Get animal details
        animal_ids = [ObjectId(ad['animal_id']) for ad in adoptions]
        animals = list(clean_db.animals.find({'_id': {'$in': animal_ids}}))
        assert len(animals) == 2
    
    def test_search_medical_records_by_animal(self, clean_db, sample_animal):
        """Test finding all medical records for a specific animal"""
        # Create multiple medical records
        records = [
            {
                'animal_id': str(sample_animal['_id']),
                'vet_name': 'Dr. Smith',
                'visit_date': '2024-01-01',
                'diagnosis': 'Checkup',
                'treatment': 'Vaccination'
            },
            {
                'animal_id': str(sample_animal['_id']),
                'vet_name': 'Dr. Jones',
                'visit_date': '2024-02-01',
                'diagnosis': 'Illness',
                'treatment': 'Medication'
            }
        ]
        clean_db.medical_records.insert_many(records)
        
        # Search for medical records
        records = list(clean_db.medical_records.find({'animal_id': str(sample_animal['_id'])}))
        assert len(records) == 2
    
    def test_search_empty_results(self, clean_db):
        """Test search with no results (edge case)"""
        fake_id = str(ObjectId())
        adoptions = list(clean_db.adoptions.find({'adopter_id': fake_id}))
        assert len(adoptions) == 0
        
        records = list(clean_db.medical_records.find({'animal_id': fake_id}))
        assert len(records) == 0
    
    def test_search_with_special_characters(self, clean_db):
        """Test search with special characters in names (edge case)"""
        animal = {
            'name': "O'Brien's Pet",
            'species': 'Dog',
            'age': 1,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(animal)
        assert result.inserted_id is not None
        
        found = clean_db.animals.find_one({'_id': result.inserted_id})
        assert found['name'] == "O'Brien's Pet"


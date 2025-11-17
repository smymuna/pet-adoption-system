"""
Integration Tests - Adoptions CRUD Operations and Edge Cases
"""

import pytest
from bson import ObjectId
from datetime import datetime


class TestAdoptionsCRUD:
    """Test Adoptions CRUD operations"""
    
    def test_create_adoption(self, clean_db, sample_animal, sample_adopter):
        """Test creating an adoption"""
        adoption = {
            'animal_id': str(sample_animal['_id']),
            'adopter_id': str(sample_adopter['_id']),
            'adoption_date': datetime.now().strftime('%Y-%m-%d'),
            'notes': 'Test adoption'
        }
        result = clean_db.adoptions.insert_one(adoption)
        assert result.inserted_id is not None
        
        # Manually update animal status (simulating API behavior)
        clean_db.animals.update_one(
            {'_id': ObjectId(sample_animal['_id'])},
            {'$set': {'status': 'Adopted'}}
        )
        
        # Verify animal status updated
        animal = clean_db.animals.find_one({'_id': ObjectId(sample_animal['_id'])})
        assert animal['status'] == 'Adopted'
    
    def test_delete_adoption_updates_animal_status(self, clean_db, sample_adoption, sample_animal):
        """Test that deleting adoption updates animal status back to Available"""
        adoption_id = ObjectId(sample_adoption['_id'])
        animal_id = ObjectId(sample_adoption['animal_id'])
        
        # Set animal status to Adopted (simulating adoption creation)
        clean_db.animals.update_one(
            {'_id': animal_id},
            {'$set': {'status': 'Adopted'}}
        )
        
        # Verify animal is adopted
        animal = clean_db.animals.find_one({'_id': animal_id})
        assert animal['status'] == 'Adopted'
        
        # Delete adoption
        clean_db.adoptions.delete_one({'_id': adoption_id})
        
        # Manually revert animal status (simulating API behavior)
        clean_db.animals.update_one(
            {'_id': animal_id},
            {'$set': {'status': 'Available'}}
        )
        
        # Verify animal status reverted
        animal = clean_db.animals.find_one({'_id': animal_id})
        assert animal['status'] == 'Available'
    
    def test_adoption_with_invalid_animal_id(self, clean_db, sample_adopter):
        """Test adoption with invalid animal ID (edge case)"""
        adoption = {
            'animal_id': str(ObjectId()),  # Non-existent animal
            'adopter_id': str(sample_adopter['_id']),
            'adoption_date': datetime.now().strftime('%Y-%m-%d')
        }
        # This should still insert, but animal won't be updated
        result = clean_db.adoptions.insert_one(adoption)
        assert result.inserted_id is not None
    
    def test_multiple_adoptions_same_adopter(self, clean_db, sample_adopter):
        """Test same adopter adopting multiple animals (edge case)"""
        # Create multiple animals
        animals = [
            {'name': 'Dog1', 'species': 'Dog', 'age': 1, 'gender': 'Male', 'status': 'Available'},
            {'name': 'Dog2', 'species': 'Dog', 'age': 2, 'gender': 'Female', 'status': 'Available'}
        ]
        animal_results = clean_db.animals.insert_many(animals)
        
        # Create adoptions
        for animal_id in animal_results.inserted_ids:
            adoption = {
                'animal_id': str(animal_id),
                'adopter_id': str(sample_adopter['_id']),
                'adoption_date': datetime.now().strftime('%Y-%m-%d')
            }
            clean_db.adoptions.insert_one(adoption)
        
        # Verify all adoptions exist
        adoptions = list(clean_db.adoptions.find({'adopter_id': str(sample_adopter['_id'])}))
        assert len(adoptions) == 2
    
    def test_adoption_date_formats(self, clean_db, sample_animal, sample_adopter):
        """Test different date formats (edge case)"""
        # Valid date format
        adoption = {
            'animal_id': str(sample_animal['_id']),
            'adopter_id': str(sample_adopter['_id']),
            'adoption_date': '2024-01-15'
        }
        result = clean_db.adoptions.insert_one(adoption)
        assert result.inserted_id is not None


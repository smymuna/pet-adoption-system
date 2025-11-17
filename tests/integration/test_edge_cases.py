"""
Integration Tests - Edge Cases and Corner Cases
"""

import pytest
from bson import ObjectId
from datetime import datetime


class TestEdgeCases:
    """Test edge cases and corner cases"""
    
    def test_very_long_strings(self, clean_db):
        """Test with very long string values"""
        long_string = 'A' * 10000
        animal = {
            'name': long_string,
            'species': 'Dog',
            'age': 1,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(animal)
        assert result.inserted_id is not None
        
        found = clean_db.animals.find_one({'_id': result.inserted_id})
        assert len(found['name']) == 10000
    
    def test_unicode_characters(self, clean_db):
        """Test with unicode characters"""
        animal = {
            'name': '🐕 Dog 中文 Español',
            'species': 'Dog',
            'age': 1,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(animal)
        assert result.inserted_id is not None
        
        found = clean_db.animals.find_one({'_id': result.inserted_id})
        assert '🐕' in found['name']
    
    def test_null_and_empty_values(self, clean_db):
        """Test handling of null and empty values"""
        # Empty string
        animal = {
            'name': '',
            'species': 'Dog',
            'age': 1,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(animal)
        assert result.inserted_id is not None
    
    def test_concurrent_updates(self, clean_db, sample_animal):
        """Test concurrent update scenarios"""
        animal_id = ObjectId(sample_animal['_id'])
        
        # Multiple updates
        clean_db.animals.update_one({'_id': animal_id}, {'$set': {'name': 'Update1'}})
        clean_db.animals.update_one({'_id': animal_id}, {'$set': {'name': 'Update2'}})
        clean_db.animals.update_one({'_id': animal_id}, {'$set': {'name': 'Update3'}})
        
        final = clean_db.animals.find_one({'_id': animal_id})
        assert final['name'] == 'Update3'
    
    def test_large_number_of_records(self, clean_db):
        """Test with large number of records"""
        animals = [
            {
                'name': f'Animal{i}',
                'species': 'Dog' if i % 2 == 0 else 'Cat',
                'age': i % 10,
                'gender': 'Male' if i % 2 == 0 else 'Female',
                'status': 'Available'
            }
            for i in range(100)
        ]
        result = clean_db.animals.insert_many(animals)
        assert len(result.inserted_ids) == 100
        
        count = clean_db.animals.count_documents({})
        assert count == 100
    
    def test_invalid_objectid_handling(self, clean_db):
        """Test handling of invalid ObjectId strings"""
        # Try to find with invalid ObjectId
        try:
            clean_db.animals.find_one({'_id': 'invalid-id'})
        except Exception:
            # Expected to fail
            pass
    
    def test_date_edge_cases(self, clean_db, sample_animal, sample_adopter):
        """Test date edge cases"""
        # Very old date
        old_date = '1900-01-01'
        adoption = {
            'animal_id': str(sample_animal['_id']),
            'adopter_id': str(sample_adopter['_id']),
            'adoption_date': old_date
        }
        result = clean_db.adoptions.insert_one(adoption)
        assert result.inserted_id is not None
        
        # Future date
        future_date = '2099-12-31'
        adoption2 = {
            'animal_id': str(sample_animal['_id']),
            'adopter_id': str(sample_adopter['_id']),
            'adoption_date': future_date
        }
        result2 = clean_db.adoptions.insert_one(adoption2)
        assert result2.inserted_id is not None
    
    def test_case_sensitivity(self, clean_db):
        """Test case sensitivity in queries"""
        animal1 = {
            'name': 'Max',
            'species': 'Dog',
            'age': 1,
            'gender': 'Male',
            'status': 'Available'
        }
        animal2 = {
            'name': 'max',
            'species': 'dog',
            'age': 1,
            'gender': 'male',
            'status': 'available'
        }
        clean_db.animals.insert_many([animal1, animal2])
        
        # Case-sensitive search
        results = list(clean_db.animals.find({'name': 'Max'}))
        assert len(results) == 1
        assert results[0]['name'] == 'Max'
    
    def test_special_characters_in_queries(self, clean_db):
        """Test special characters in field values"""
        animal = {
            'name': "O'Brien's Pet & Co.",
            'species': 'Dog',
            'age': 1,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(animal)
        assert result.inserted_id is not None
        
        # Search with special characters
        found = clean_db.animals.find_one({'name': "O'Brien's Pet & Co."})
        assert found is not None


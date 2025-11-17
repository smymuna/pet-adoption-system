"""
Integration Tests - Animals CRUD Operations
"""

import pytest
from bson import ObjectId
from backend.database.connection import serialize_doc


class TestAnimalsCRUD:
    """Test Animals CRUD operations"""
    
    def test_create_animal(self, clean_db):
        """Test creating an animal"""
        animal = {
            'name': 'Max',
            'species': 'Dog',
            'age': 4,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(animal)
        assert result.inserted_id is not None
        
        # Verify creation
        created = clean_db.animals.find_one({'_id': result.inserted_id})
        assert created['name'] == 'Max'
        assert created['species'] == 'Dog'
        assert created['age'] == 4
    
    def test_read_animal(self, clean_db, sample_animal):
        """Test reading an animal"""
        animal = clean_db.animals.find_one({'_id': ObjectId(sample_animal['_id'])})
        assert animal is not None
        assert animal['name'] == 'Test Dog'
    
    def test_read_all_animals(self, clean_db):
        """Test reading all animals"""
        # Create multiple animals
        animals = [
            {'name': 'Dog1', 'species': 'Dog', 'age': 1, 'gender': 'Male', 'status': 'Available'},
            {'name': 'Cat1', 'species': 'Cat', 'age': 2, 'gender': 'Female', 'status': 'Available'},
            {'name': 'Dog2', 'species': 'Dog', 'age': 3, 'gender': 'Male', 'status': 'Adopted'}
        ]
        clean_db.animals.insert_many(animals)
        
        all_animals = list(clean_db.animals.find())
        assert len(all_animals) == 3
    
    def test_update_animal(self, clean_db, sample_animal):
        """Test updating an animal"""
        animal_id = ObjectId(sample_animal['_id'])
        clean_db.animals.update_one(
            {'_id': animal_id},
            {'$set': {'name': 'Updated Name', 'age': 5}}
        )
        
        updated = clean_db.animals.find_one({'_id': animal_id})
        assert updated['name'] == 'Updated Name'
        assert updated['age'] == 5
        assert updated['species'] == 'Dog'  # Unchanged field
    
    def test_delete_animal(self, clean_db, sample_animal):
        """Test deleting an animal"""
        animal_id = ObjectId(sample_animal['_id'])
        result = clean_db.animals.delete_one({'_id': animal_id})
        assert result.deleted_count == 1
        
        # Verify deletion
        deleted = clean_db.animals.find_one({'_id': animal_id})
        assert deleted is None
    
    def test_create_animal_edge_cases(self, clean_db):
        """Test edge cases for animal creation"""
        # Very long name
        long_name = 'A' * 1000
        animal = {
            'name': long_name,
            'species': 'Dog',
            'age': 1,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(animal)
        assert result.inserted_id is not None
        
        # Very old animal
        old_animal = {
            'name': 'Old Dog',
            'species': 'Dog',
            'age': 20,
            'gender': 'Male',
            'status': 'Available'
        }
        result = clean_db.animals.insert_one(old_animal)
        assert result.inserted_id is not None
    
    def test_update_nonexistent_animal(self, clean_db):
        """Test updating non-existent animal (edge case)"""
        fake_id = ObjectId()
        result = clean_db.animals.update_one(
            {'_id': fake_id},
            {'$set': {'name': 'Test'}}
        )
        assert result.matched_count == 0
        assert result.modified_count == 0
    
    def test_delete_nonexistent_animal(self, clean_db):
        """Test deleting non-existent animal (edge case)"""
        fake_id = ObjectId()
        result = clean_db.animals.delete_one({'_id': fake_id})
        assert result.deleted_count == 0
    
    def test_animal_status_transitions(self, clean_db, sample_animal):
        """Test animal status transitions"""
        animal_id = ObjectId(sample_animal['_id'])
        
        # Available -> Adopted
        clean_db.animals.update_one({'_id': animal_id}, {'$set': {'status': 'Adopted'}})
        animal = clean_db.animals.find_one({'_id': animal_id})
        assert animal['status'] == 'Adopted'
        
        # Adopted -> Available
        clean_db.animals.update_one({'_id': animal_id}, {'$set': {'status': 'Available'}})
        animal = clean_db.animals.find_one({'_id': animal_id})
        assert animal['status'] == 'Available'
        
        # Available -> Medical
        clean_db.animals.update_one({'_id': animal_id}, {'$set': {'status': 'Medical'}})
        animal = clean_db.animals.find_one({'_id': animal_id})
        assert animal['status'] == 'Medical'


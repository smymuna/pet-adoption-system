"""
Unit Tests - Pydantic Models
"""

import pytest
from pydantic import ValidationError

from backend.models import (
    AnimalCreate, AnimalUpdate, AnimalResponse,
    AdopterCreate, AdopterUpdate, AdopterResponse,
    AdoptionCreate, AdoptionUpdate, AdoptionResponse,
    MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse,
    VolunteerCreate, VolunteerUpdate, VolunteerResponse,
    SuccessResponse
)


class TestAnimalModels:
    """Test Animal model validation"""
    
    def test_animal_create_valid(self):
        """Test valid animal creation"""
        animal = AnimalCreate(
            name="Buddy",
            species="Dog",
            age=3,
            gender="Male",
            status="Available"
        )
        assert animal.name == "Buddy"
        assert animal.species == "Dog"
        assert animal.age == 3
        assert animal.gender == "Male"
        assert animal.status == "Available"
    
    def test_animal_create_default_status(self):
        """Test animal creation with default status"""
        animal = AnimalCreate(
            name="Luna",
            species="Cat",
            age=2,
            gender="Female"
        )
        assert animal.status == "Available"
    
    def test_animal_create_invalid_age(self):
        """Test animal creation with invalid age (edge case)"""
        with pytest.raises(ValidationError):
            AnimalCreate(
                name="Test",
                species="Dog",
                age=-1,  # Negative age
                gender="Male"
            )
    
    def test_animal_create_zero_age(self):
        """Test animal creation with zero age (edge case)"""
        with pytest.raises(ValidationError):
            AnimalCreate(
                name="Test",
                species="Dog",
                age=0,  # Zero age
                gender="Male"
            )
    
    def test_animal_update_partial(self):
        """Test partial animal update"""
        update = AnimalUpdate(name="New Name")
        assert update.name == "New Name"
        assert update.species is None
        assert update.age is None
    
    def test_animal_update_empty(self):
        """Test empty animal update (edge case)"""
        update = AnimalUpdate()
        assert update.name is None
        assert update.species is None


class TestAdopterModels:
    """Test Adopter model validation"""
    
    def test_adopter_create_valid(self):
        """Test valid adopter creation"""
        adopter = AdopterCreate(
            name="John Doe",
            phone="555-1234",
            email="john@example.com",
            address="123 Main St"
        )
        assert adopter.email == "john@example.com"
    
    def test_adopter_create_invalid_email(self):
        """Test adopter creation with invalid email (edge case)"""
        with pytest.raises(ValidationError):
            AdopterCreate(
                name="John",
                phone="555-1234",
                email="invalid-email",  # Invalid email format
                address="123 Main St"
            )
    
    def test_adopter_create_empty_email(self):
        """Test adopter creation with empty email (edge case)"""
        with pytest.raises(ValidationError):
            AdopterCreate(
                name="John",
                phone="555-1234",
                email="",  # Empty email
                address="123 Main St"
            )


class TestAdoptionModels:
    """Test Adoption model validation"""
    
    def test_adoption_create_valid(self):
        """Test valid adoption creation"""
        adoption = AdoptionCreate(
            animal_id="507f1f77bcf86cd799439011",
            adopter_id="507f1f77bcf86cd799439012"
        )
        assert adoption.animal_id is not None
        assert adoption.adopter_id is not None
    
    def test_adoption_create_with_notes(self):
        """Test adoption creation with notes"""
        adoption = AdoptionCreate(
            animal_id="507f1f77bcf86cd799439011",
            adopter_id="507f1f77bcf86cd799439012",
            notes="Great match!"
        )
        assert adoption.notes == "Great match!"


class TestSuccessResponse:
    """Test SuccessResponse model"""
    
    def test_success_response(self):
        """Test success response creation"""
        response = SuccessResponse(success=True, message="Operation successful")
        assert response.success is True
        assert response.message == "Operation successful"
    
    def test_failure_response(self):
        """Test failure response creation"""
        response = SuccessResponse(success=False, message="Operation failed")
        assert response.success is False
        assert response.message == "Operation failed"


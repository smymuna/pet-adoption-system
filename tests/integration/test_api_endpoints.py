"""
Integration Tests - API Endpoints
Tests FastAPI routes using TestClient
"""

import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main import app
from backend.database.connection import get_database

# Create client
client = TestClient(app, follow_redirects=False)


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_redirect(self):
        """Test root endpoint redirects to dashboard"""
        response = client.get("/")
        assert response.status_code == 307  # Redirect
    
    def test_dashboard_page(self):
        """Test dashboard page loads"""
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_animals_page(self):
        """Test animals page loads"""
        response = client.get("/animals")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_get_animals_api(self, clean_db):
        """Test GET /api/animals endpoint"""
        # Ensure database has valid data
        clean_db.animals.delete_many({})
        clean_db.animals.insert_one({
            'name': 'Test Dog',
            'species': 'Dog',
            'age': 3,
            'gender': 'Male',
            'status': 'Available'
        })
        
        # Mock get_database to return test database
        with patch('backend.api.routes.animals.get_database', return_value=clean_db):
            response = client.get("/api/animals")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            if len(data) > 0:
                assert 'species' in data[0]
    
    def test_create_animal_api(self, clean_db):
        """Test POST /api/animals endpoint"""
        clean_db.animals.delete_many({})
        animal_data = {
            "name": "API Test Dog",
            "species": "Dog",
            "age": 2,
            "gender": "Male",
            "status": "Available"
        }
        # Mock get_database to return test database
        with patch('backend.api.routes.animals.get_database', return_value=clean_db):
            response = client.post("/api/animals", json=animal_data)
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "API Test Dog"
            assert "_id" in data
    
    def test_get_animal_by_id_api(self, clean_db, sample_animal):
        """Test GET /api/animals/{id} endpoint"""
        # Ensure animal exists in database
        clean_db.animals.delete_many({})
        animal_id = ObjectId(sample_animal['_id'])
        clean_db.animals.insert_one({
            '_id': animal_id,
            'name': sample_animal['name'],
            'species': sample_animal['species'],
            'age': sample_animal['age'],
            'gender': sample_animal['gender'],
            'status': sample_animal['status']
        })
        
        # Mock get_database to return test database
        with patch('backend.api.routes.animals.get_database', return_value=clean_db):
            response = client.get(f"/api/animals/{sample_animal['_id']}")
            assert response.status_code == 200
            data = response.json()
            assert data["_id"] == sample_animal["_id"]
    
    def test_get_nonexistent_animal_api(self, clean_db):
        """Test GET /api/animals/{id} with non-existent ID"""
        # Ensure database is clean
        clean_db.animals.delete_many({})
        fake_id = str(ObjectId())
        # Mock get_database to return test database
        with patch('backend.api.routes.animals.get_database', return_value=clean_db):
            response = client.get(f"/api/animals/{fake_id}")
            assert response.status_code == 404
    
    def test_update_animal_api(self, clean_db, sample_animal):
        """Test PUT /api/animals/{id} endpoint"""
        # Ensure animal exists in database
        clean_db.animals.delete_many({})
        animal_id = ObjectId(sample_animal['_id'])
        clean_db.animals.insert_one({
            '_id': animal_id,
            'name': sample_animal['name'],
            'species': sample_animal['species'],
            'age': sample_animal['age'],
            'gender': sample_animal['gender'],
            'status': sample_animal['status']
        })
        
        update_data = {"name": "Updated Name", "age": 5}
        # Mock get_database to return test database
        with patch('backend.api.routes.animals.get_database', return_value=clean_db):
            response = client.put(f"/api/animals/{sample_animal['_id']}", json=update_data)
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Updated Name"
            assert data["age"] == 5
    
    def test_delete_animal_api(self, clean_db, sample_animal):
        """Test DELETE /api/animals/{id} endpoint"""
        # Ensure animal exists in database
        clean_db.animals.delete_many({})
        animal_id = ObjectId(sample_animal['_id'])
        clean_db.animals.insert_one({
            '_id': animal_id,
            'name': sample_animal['name'],
            'species': sample_animal['species'],
            'age': sample_animal['age'],
            'gender': sample_animal['gender'],
            'status': sample_animal['status']
        })
        
        # Mock get_database to return test database
        with patch('backend.api.routes.animals.get_database', return_value=clean_db):
            response = client.delete(f"/api/animals/{sample_animal['_id']}")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            
            # Verify deletion
            get_response = client.get(f"/api/animals/{sample_animal['_id']}")
            assert get_response.status_code == 404
    
    def test_create_animal_invalid_data(self):
        """Test POST /api/animals with invalid data (edge case)"""
        invalid_data = {
            "name": "Test",
            "species": "Dog",
            "age": -1,  # Invalid age
            "gender": "Male"
        }
        response = client.post("/api/animals", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_charts_species_api(self, clean_db):
        """Test GET /api/charts/species endpoint"""
        # Ensure database has valid data
        clean_db.animals.delete_many({})
        clean_db.animals.insert_many([
            {'name': 'Dog1', 'species': 'Dog', 'age': 1, 'gender': 'Male', 'status': 'Available'},
            {'name': 'Dog2', 'species': 'Dog', 'age': 2, 'gender': 'Female', 'status': 'Available'},
            {'name': 'Cat1', 'species': 'Cat', 'age': 3, 'gender': 'Male', 'status': 'Available'}
        ])
        
        # Mock get_database to return test database
        with patch('backend.api.routes.charts.get_database', return_value=clean_db):
            response = client.get("/api/charts/species")
            assert response.status_code == 200
            data = response.json()
            assert "labels" in data
            assert "data" in data
            assert isinstance(data["labels"], list)
            assert isinstance(data["data"], list)
    
    def test_charts_adoptions_api(self):
        """Test GET /api/charts/adoptions endpoint"""
        response = client.get("/api/charts/adoptions")
        assert response.status_code == 200
        data = response.json()
        assert "labels" in data
        assert "data" in data
        assert isinstance(data["labels"], list)
        assert isinstance(data["data"], list)
    
    def test_search_by_adopter_api(self, clean_db, sample_adopter):
        """Test GET /api/search/adopter/{id} endpoint"""
        response = client.get(f"/api/search/adopter/{sample_adopter['_id']}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_medical_api(self, clean_db, sample_animal):
        """Test GET /api/search/medical/{id} endpoint"""
        response = client.get(f"/api/search/medical/{sample_animal['_id']}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


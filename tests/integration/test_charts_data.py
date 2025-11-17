"""
Integration Tests - Charts Data Aggregation
"""

import pytest
from collections import Counter
from datetime import datetime


class TestChartsData:
    """Test data aggregation for charts"""
    
    def test_species_distribution(self, clean_db):
        """Test species distribution calculation"""
        animals = [
            {'name': 'Dog1', 'species': 'Dog', 'age': 1, 'gender': 'Male', 'status': 'Available'},
            {'name': 'Dog2', 'species': 'Dog', 'age': 2, 'gender': 'Female', 'status': 'Available'},
            {'name': 'Cat1', 'species': 'Cat', 'age': 3, 'gender': 'Male', 'status': 'Available'},
            {'name': 'Bird1', 'species': 'Bird', 'age': 1, 'gender': 'Male', 'status': 'Available'}
        ]
        clean_db.animals.insert_many(animals)
        
        all_animals = list(clean_db.animals.find())
        species_count = Counter(animal['species'] for animal in all_animals)
        
        assert species_count['Dog'] == 2
        assert species_count['Cat'] == 1
        assert species_count['Bird'] == 1
    
    def test_monthly_adoptions(self, clean_db, sample_adopter):
        """Test monthly adoption aggregation"""
        # Create animals
        animals = [
            {'name': 'Dog1', 'species': 'Dog', 'age': 1, 'gender': 'Male', 'status': 'Available'},
            {'name': 'Dog2', 'species': 'Dog', 'age': 2, 'gender': 'Female', 'status': 'Available'},
            {'name': 'Cat1', 'species': 'Cat', 'age': 3, 'gender': 'Male', 'status': 'Available'}
        ]
        animal_results = clean_db.animals.insert_many(animals)
        
        # Create adoptions in different months
        adoptions = [
            {
                'animal_id': str(animal_results.inserted_ids[0]),
                'adopter_id': str(sample_adopter['_id']),
                'adoption_date': '2024-01-15'
            },
            {
                'animal_id': str(animal_results.inserted_ids[1]),
                'adopter_id': str(sample_adopter['_id']),
                'adoption_date': '2024-01-20'
            },
            {
                'animal_id': str(animal_results.inserted_ids[2]),
                'adopter_id': str(sample_adopter['_id']),
                'adoption_date': '2024-02-10'
            }
        ]
        clean_db.adoptions.insert_many(adoptions)
        
        # Calculate monthly adoptions
        all_adoptions = list(clean_db.adoptions.find())
        monthly_count = Counter()
        
        for adoption in all_adoptions:
            adoption_date = adoption.get('adoption_date', '')
            if adoption_date:
                try:
                    date_obj = datetime.strptime(adoption_date, '%Y-%m-%d')
                    month_key = date_obj.strftime('%Y-%m')
                    monthly_count[month_key] += 1
                except:
                    pass
        
        assert monthly_count['2024-01'] == 2
        assert monthly_count['2024-02'] == 1
    
    def test_empty_data_charts(self, clean_db):
        """Test charts with empty data (edge case)"""
        all_animals = list(clean_db.animals.find())
        species_count = Counter(animal['species'] for animal in all_animals)
        
        assert len(species_count) == 0
        
        all_adoptions = list(clean_db.adoptions.find())
        monthly_count = Counter()
        for adoption in all_adoptions:
            adoption_date = adoption.get('adoption_date', '')
            if adoption_date:
                try:
                    date_obj = datetime.strptime(adoption_date, '%Y-%m-%d')
                    month_key = date_obj.strftime('%Y-%m')
                    monthly_count[month_key] += 1
                except:
                    pass
        
        assert len(monthly_count) == 0


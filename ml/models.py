"""
Machine Learning Models
Enhanced adoption likelihood and time-to-adoption prediction models
Now includes: breed, time-in-shelter, and medical history
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'saved_models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Model paths
ADOPTION_LIKELIHOOD_MODEL_PATH = os.path.join(MODELS_DIR, 'adoption_likelihood_model.pkl')
TIME_TO_ADOPTION_MODEL_PATH = os.path.join(MODELS_DIR, 'time_to_adoption_model.pkl')
SPECIES_ENCODER_PATH = os.path.join(MODELS_DIR, 'species_encoder.pkl')
BREED_ENCODER_PATH = os.path.join(MODELS_DIR, 'breed_encoder.pkl')
GENDER_ENCODER_PATH = os.path.join(MODELS_DIR, 'gender_encoder.pkl')
STATUS_ENCODER_PATH = os.path.join(MODELS_DIR, 'status_encoder.pkl')
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, 'feature_names.pkl')

# Initialize encoders
species_encoder = LabelEncoder()
breed_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
status_encoder = LabelEncoder()


def calculate_days_in_shelter(intake_date_str, reference_date=None):
    """Calculate days in shelter from intake date"""
    if not intake_date_str:
        return None
    
    try:
        intake_date = datetime.strptime(intake_date_str, '%Y-%m-%d')
        if reference_date is None:
            reference_date = datetime.now()
        elif isinstance(reference_date, str):
            reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
        
        days = (reference_date - intake_date).days
        return max(0, days)  # Ensure non-negative
    except:
        return None


def prepare_adoption_data(db):
    """Prepare data for adoption likelihood model with enhanced features"""
    animals = list(db.animals.find())
    adoptions = list(db.adoptions.find())
    medical_records = list(db.medical_records.find())
    
    if len(animals) < 10:
        return None, None, None
    
    # Create adoption status for each animal
    adoption_dict = {str(ad['animal_id']): True for ad in adoptions}
    
    # Count medical records per animal
    medical_count = {}
    for record in medical_records:
        animal_id = str(record.get('animal_id', ''))
        medical_count[animal_id] = medical_count.get(animal_id, 0) + 1
    
    # Get latest adoption date for reference
    latest_adoption_date = None
    for adoption in adoptions:
        adoption_date = adoption.get('adoption_date', '')
        if adoption_date:
            try:
                date_obj = datetime.strptime(adoption_date, '%Y-%m-%d')
                if latest_adoption_date is None or date_obj > latest_adoption_date:
                    latest_adoption_date = date_obj
            except:
                pass
    
    if latest_adoption_date is None:
        latest_adoption_date = datetime.now()
    
    data = []
    for animal in animals:
        animal_id = str(animal['_id'])
        intake_date = animal.get('intake_date', '')
        
        # Calculate days in shelter
        days_in_shelter = calculate_days_in_shelter(intake_date, latest_adoption_date)
        if days_in_shelter is None:
            # If no intake date, use 0 (newly arrived)
            days_in_shelter = 0
        
        data.append({
            'species': animal.get('species', 'Unknown'),
            'breed': animal.get('breed', 'Unknown'),
            'age': animal.get('age', 0),
            'gender': animal.get('gender', 'Unknown'),
            'status': animal.get('status', 'Available'),
            'days_in_shelter': days_in_shelter,
            'medical_count': medical_count.get(animal_id, 0),
            'adopted': adoption_dict.get(animal_id, False)
        })
    
    df = pd.DataFrame(data)
    
    # Encode categorical variables
    df['species_encoded'] = species_encoder.fit_transform(df['species'])
    df['breed_encoded'] = breed_encoder.fit_transform(df['breed'])
    df['gender_encoded'] = gender_encoder.fit_transform(df['gender'])
    df['status_encoded'] = status_encoder.fit_transform(df['status'])
    
    # Feature columns: species, breed, age, gender, status, days_in_shelter, medical_count
    feature_names = ['species_encoded', 'breed_encoded', 'age', 'gender_encoded', 
                    'status_encoded', 'days_in_shelter', 'medical_count']
    X = df[feature_names]
    y = df['adopted'].astype(int)
    
    return X, y, feature_names


def prepare_time_data(db):
    """Prepare data for time-to-adoption model with enhanced features"""
    animals = list(db.animals.find())
    adoptions = list(db.adoptions.find())
    medical_records = list(db.medical_records.find())
    
    if len(adoptions) < 5:
        return None, None, None
    
    # Create a mapping of animal_id to adoption date
    adoption_dates = {}
    for adoption in adoptions:
        animal_id = str(adoption['animal_id'])
        adoption_date = adoption.get('adoption_date', '')
        if adoption_date:
            try:
                adoption_dates[animal_id] = datetime.strptime(adoption_date, '%Y-%m-%d')
            except:
                pass
    
    # Count medical records per animal (before adoption)
    medical_count = {}
    for record in medical_records:
        animal_id = str(record.get('animal_id', ''))
        if animal_id in adoption_dates:
            visit_date = record.get('visit_date', '')
            if visit_date:
                try:
                    visit_dt = datetime.strptime(visit_date, '%Y-%m-%d')
                    adoption_dt = adoption_dates.get(animal_id)
                    if adoption_dt and visit_dt <= adoption_dt:
                        medical_count[animal_id] = medical_count.get(animal_id, 0) + 1
                except:
                    pass
    
    data = []
    for animal in animals:
        animal_id = str(animal['_id'])
        if animal_id in adoption_dates:
            intake_date_str = animal.get('intake_date', '')
            adoption_date = adoption_dates[animal_id]
            
            # Calculate actual days to adoption
            if intake_date_str:
                try:
                    intake_date = datetime.strptime(intake_date_str, '%Y-%m-%d')
                    days_to_adoption = (adoption_date - intake_date).days
                except:
                    # Fallback: estimate 30 days if intake date invalid
                    days_to_adoption = 30
            else:
                # No intake date, estimate 30 days
                days_to_adoption = 30
            
            days_to_adoption = max(1, days_to_adoption)  # At least 1 day
            
            data.append({
                'species': animal.get('species', 'Unknown'),
                'breed': animal.get('breed', 'Unknown'),
                'age': animal.get('age', 0),
                'gender': animal.get('gender', 'Unknown'),
                'days_in_shelter': days_to_adoption,  # This is actually days to adoption
                'medical_count': medical_count.get(animal_id, 0),
                'days_to_adoption': days_to_adoption
            })
    
    if len(data) < 5:
        return None, None, None
    
    df = pd.DataFrame(data)
    df['species_encoded'] = species_encoder.transform(df['species'])
    df['breed_encoded'] = breed_encoder.transform(df['breed'])
    df['gender_encoded'] = gender_encoder.transform(df['gender'])
    
    # Feature columns: species, breed, age, gender, days_in_shelter (at time of adoption), medical_count
    feature_names = ['species_encoded', 'breed_encoded', 'age', 'gender_encoded', 
                    'days_in_shelter', 'medical_count']
    X = df[feature_names]
    y = df['days_to_adoption']
    
    return X, y, feature_names


def train_all_models(db):
    """Train all ML models with feature importance tracking"""
    results = {}
    
    # Train adoption likelihood model
    try:
        X, y, feature_names = prepare_adoption_data(db)
        if X is not None and len(X) >= 10:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)
            
            # Get feature importance
            feature_importance = dict(zip(feature_names, model.feature_importances_))
            
            joblib.dump(model, ADOPTION_LIKELIHOOD_MODEL_PATH)
            joblib.dump(species_encoder, SPECIES_ENCODER_PATH)
            joblib.dump(breed_encoder, BREED_ENCODER_PATH)
            joblib.dump(gender_encoder, GENDER_ENCODER_PATH)
            joblib.dump(status_encoder, STATUS_ENCODER_PATH)
            joblib.dump(feature_names, FEATURE_NAMES_PATH)
            
            results['adoption_likelihood'] = {
                'trained': True,
                'accuracy': round(accuracy * 100, 2),
                'feature_importance': {k: round(v, 4) for k, v in feature_importance.items()}
            }
        else:
            results['adoption_likelihood'] = {
                'trained': False,
                'message': 'Insufficient data (need at least 10 animals)'
            }
    except Exception as e:
        results['adoption_likelihood'] = {
            'trained': False,
            'error': str(e)
        }
    
    # Train time-to-adoption model
    try:
        X, y, feature_names = prepare_time_data(db)
        if X is not None and len(X) >= 5:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            r2 = model.score(X_test, y_test)
            
            # Get feature importance
            feature_importance = dict(zip(feature_names, model.feature_importances_))
            
            joblib.dump(model, TIME_TO_ADOPTION_MODEL_PATH)
            
            results['time_to_adoption'] = {
                'trained': True,
                'r2_score': round(r2, 2),
                'feature_importance': {k: round(v, 4) for k, v in feature_importance.items()}
            }
        else:
            results['time_to_adoption'] = {
                'trained': False,
                'message': 'Insufficient adoption data (need at least 5 adoptions)'
            }
    except Exception as e:
        results['time_to_adoption'] = {
            'trained': False,
            'error': str(e)
        }
    
    return results


def predict_adoption_likelihood(animal_data, db=None):
    """Predict adoption likelihood for an animal with enhanced features"""
    if not os.path.exists(ADOPTION_LIKELIHOOD_MODEL_PATH):
        return None, None
    
    try:
        model = joblib.load(ADOPTION_LIKELIHOOD_MODEL_PATH)
        species_enc = joblib.load(SPECIES_ENCODER_PATH)
        breed_enc = joblib.load(BREED_ENCODER_PATH)
        gender_enc = joblib.load(GENDER_ENCODER_PATH)
        status_enc = joblib.load(STATUS_ENCODER_PATH)
        
        # Get medical count if db provided
        medical_count = 0
        if db:
            animal_id = animal_data.get('_id')
            if animal_id:
                medical_count = db.medical_records.count_documents({'animal_id': animal_id})
        else:
            medical_count = animal_data.get('medical_count', 0)
        
        # Calculate days in shelter
        intake_date = animal_data.get('intake_date', '')
        days_in_shelter = calculate_days_in_shelter(intake_date) or 0
        
        # Prepare features
        species_encoded = species_enc.transform([animal_data.get('species', 'Unknown')])[0]
        breed_encoded = breed_enc.transform([animal_data.get('breed', 'Unknown')])[0]
        gender_encoded = gender_enc.transform([animal_data.get('gender', 'Unknown')])[0]
        status_encoded = status_enc.transform([animal_data.get('status', 'Available')])[0]
        
        features = np.array([[
            species_encoded, 
            breed_encoded,
            animal_data.get('age', 0), 
            gender_encoded, 
            status_encoded,
            days_in_shelter,
            medical_count
        ]])
        
        # Get probability
        prob = model.predict_proba(features)[0][1]
        
        # Get feature importance if available
        feature_importance = dict(zip(
            ['species', 'breed', 'age', 'gender', 'status', 'days_in_shelter', 'medical_count'],
            model.feature_importances_
        ))
        
        return prob, feature_importance
    except Exception as e:
        print(f"Prediction error: {e}")
        return None, None


def predict_time_to_adoption(animal_data, db=None):
    """Predict time to adoption for an animal with enhanced features"""
    if not os.path.exists(TIME_TO_ADOPTION_MODEL_PATH):
        return None, None
    
    try:
        model = joblib.load(TIME_TO_ADOPTION_MODEL_PATH)
        species_enc = joblib.load(SPECIES_ENCODER_PATH)
        breed_enc = joblib.load(BREED_ENCODER_PATH)
        gender_enc = joblib.load(GENDER_ENCODER_PATH)
        
        # Get medical count if db provided
        medical_count = 0
        if db:
            animal_id = animal_data.get('_id')
            if animal_id:
                medical_count = db.medical_records.count_documents({'animal_id': animal_id})
        else:
            medical_count = animal_data.get('medical_count', 0)
        
        # Calculate days in shelter
        intake_date = animal_data.get('intake_date', '')
        days_in_shelter = calculate_days_in_shelter(intake_date) or 0
        
        # Prepare features
        species_encoded = species_enc.transform([animal_data.get('species', 'Unknown')])[0]
        breed_encoded = breed_enc.transform([animal_data.get('breed', 'Unknown')])[0]
        gender_encoded = gender_enc.transform([animal_data.get('gender', 'Unknown')])[0]
        
        features = np.array([[
            species_encoded,
            breed_encoded,
            animal_data.get('age', 0), 
            gender_encoded,
            days_in_shelter,
            medical_count
        ]])
        
        prediction = model.predict(features)[0]
        prediction = max(1, prediction)  # Ensure at least 1 day
        
        # Get feature importance if available
        feature_importance = dict(zip(
            ['species', 'breed', 'age', 'gender', 'days_in_shelter', 'medical_count'],
            model.feature_importances_
        ))
        
        return prediction, feature_importance
    except Exception as e:
        print(f"Prediction error: {e}")
        return None, None

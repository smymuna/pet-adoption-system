"""
Machine Learning Models
Adoption likelihood and time-to-adoption prediction models
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
GENDER_ENCODER_PATH = os.path.join(MODELS_DIR, 'gender_encoder.pkl')
STATUS_ENCODER_PATH = os.path.join(MODELS_DIR, 'status_encoder.pkl')

# Initialize encoders
species_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
status_encoder = LabelEncoder()


def prepare_adoption_data(db):
    """Prepare data for adoption likelihood model"""
    animals = list(db.animals.find())
    adoptions = list(db.adoptions.find())
    
    if len(animals) < 10:
        return None, None
    
    # Create adoption status for each animal
    adoption_dict = {str(ad['animal_id']): True for ad in adoptions}
    
    data = []
    for animal in animals:
        animal_id = str(animal['_id'])
        data.append({
            'species': animal.get('species', 'Unknown'),
            'age': animal.get('age', 0),
            'gender': animal.get('gender', 'Unknown'),
            'status': animal.get('status', 'Available'),
            'adopted': adoption_dict.get(animal_id, False)
        })
    
    df = pd.DataFrame(data)
    
    # Encode categorical variables
    df['species_encoded'] = species_encoder.fit_transform(df['species'])
    df['gender_encoded'] = gender_encoder.fit_transform(df['gender'])
    df['status_encoded'] = status_encoder.fit_transform(df['status'])
    
    X = df[['species_encoded', 'age', 'gender_encoded', 'status_encoded']]
    y = df['adopted'].astype(int)
    
    return X, y


def prepare_time_data(db):
    """Prepare data for time-to-adoption model"""
    animals = list(db.animals.find())
    adoptions = list(db.adoptions.find())
    
    if len(adoptions) < 5:
        return None, None
    
    # Create a mapping of animal_id to adoption date
    adoption_dates = {}
    animal_intake_dates = {}
    
    for adoption in adoptions:
        animal_id = str(adoption['animal_id'])
        adoption_date = adoption.get('adoption_date', '')
        if adoption_date:
            try:
                adoption_dates[animal_id] = datetime.strptime(adoption_date, '%Y-%m-%d')
            except:
                pass
    
    # For simplicity, assume animals were added 30 days before adoption
    # In a real system, you'd have an intake_date field
    data = []
    for animal in animals:
        animal_id = str(animal['_id'])
        if animal_id in adoption_dates:
            # Estimate intake date (30 days before adoption)
            intake_date = adoption_dates[animal_id]
            days_to_adoption = 30  # Simplified
            
            data.append({
                'species': animal.get('species', 'Unknown'),
                'age': animal.get('age', 0),
                'gender': animal.get('gender', 'Unknown'),
                'days_to_adoption': days_to_adoption
            })
    
    if len(data) < 5:
        return None, None
    
    df = pd.DataFrame(data)
    df['species_encoded'] = species_encoder.transform(df['species'])
    df['gender_encoded'] = gender_encoder.transform(df['gender'])
    
    X = df[['species_encoded', 'age', 'gender_encoded']]
    y = df['days_to_adoption']
    
    return X, y


def train_all_models(db):
    """Train all ML models"""
    results = {}
    
    # Train adoption likelihood model
    try:
        X, y = prepare_adoption_data(db)
        if X is not None and len(X) >= 10:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)
            
            joblib.dump(model, ADOPTION_LIKELIHOOD_MODEL_PATH)
            joblib.dump(species_encoder, SPECIES_ENCODER_PATH)
            joblib.dump(gender_encoder, GENDER_ENCODER_PATH)
            joblib.dump(status_encoder, STATUS_ENCODER_PATH)
            
            results['adoption_likelihood'] = {
                'trained': True,
                'accuracy': round(accuracy * 100, 2)
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
        X, y = prepare_time_data(db)
        if X is not None and len(X) >= 5:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            r2 = model.score(X_test, y_test)
            
            joblib.dump(model, TIME_TO_ADOPTION_MODEL_PATH)
            
            results['time_to_adoption'] = {
                'trained': True,
                'r2_score': round(r2, 2)
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


def predict_adoption_likelihood(animal_data):
    """Predict adoption likelihood for an animal"""
    if not os.path.exists(ADOPTION_LIKELIHOOD_MODEL_PATH):
        return None
    
    try:
        model = joblib.load(ADOPTION_LIKELIHOOD_MODEL_PATH)
        species_enc = joblib.load(SPECIES_ENCODER_PATH)
        gender_enc = joblib.load(GENDER_ENCODER_PATH)
        status_enc = joblib.load(STATUS_ENCODER_PATH)
        
        # Prepare features
        species_encoded = species_enc.transform([animal_data.get('species', 'Unknown')])[0]
        gender_encoded = gender_enc.transform([animal_data.get('gender', 'Unknown')])[0]
        status_encoded = status_enc.transform([animal_data.get('status', 'Available')])[0]
        
        features = np.array([[species_encoded, animal_data.get('age', 0), gender_encoded, status_encoded]])
        
        # Get probability
        prob = model.predict_proba(features)[0][1]
        return prob
    except Exception as e:
        print(f"Prediction error: {e}")
        return None


def predict_time_to_adoption(animal_data):
    """Predict time to adoption for an animal"""
    if not os.path.exists(TIME_TO_ADOPTION_MODEL_PATH):
        return None
    
    try:
        model = joblib.load(TIME_TO_ADOPTION_MODEL_PATH)
        species_enc = joblib.load(SPECIES_ENCODER_PATH)
        gender_enc = joblib.load(GENDER_ENCODER_PATH)
        
        # Prepare features
        species_encoded = species_enc.transform([animal_data.get('species', 'Unknown')])[0]
        gender_encoded = gender_enc.transform([animal_data.get('gender', 'Unknown')])[0]
        
        features = np.array([[species_encoded, animal_data.get('age', 0), gender_encoded]])
        
        prediction = model.predict(features)[0]
        return max(0, prediction)  # Ensure non-negative
    except Exception as e:
        print(f"Prediction error: {e}")
        return None


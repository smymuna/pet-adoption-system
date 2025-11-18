"""
ML Predictions Routes
Machine Learning prediction endpoints
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List, Dict, Optional
import os

from backend.database.connection import get_database, serialize_doc
from ml.models import train_all_models, calculate_priority_score, predict_time_to_adoption

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Model file paths - use same paths as ml/models.py
MODELS_DIR = os.path.join(os.path.dirname(__file__), '../../ml/saved_models')
ADOPTION_LIKELIHOOD_MODEL_PATH = os.path.join(MODELS_DIR, 'adoption_likelihood_model.pkl')
TIME_TO_ADOPTION_MODEL_PATH = os.path.join(MODELS_DIR, 'time_to_adoption_model.pkl')


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def ml_predictions_page(request: Request):
    """Render ML predictions page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    animals_list = [serialize_doc(a) for a in db.animals.find({'status': 'Available'})]
    
    # Check if models exist
    likelihood_model_exists = os.path.exists(ADOPTION_LIKELIHOOD_MODEL_PATH)
    time_model_exists = os.path.exists(TIME_TO_ADOPTION_MODEL_PATH)
    
    # Get model status
    model_status = {
        'adoption_likelihood_trained': likelihood_model_exists,
        'time_to_adoption_trained': time_model_exists
    }
    
    return templates.TemplateResponse("ml_predictions.html", {
        "request": request, 
        "animals": animals_list,
        "model_status": model_status
    })


@router.post("/train", response_model=Dict)
async def train_models():
    """Train ML models"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        result = train_all_models(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/predictions", response_model=List[Dict])
async def get_all_predictions():
    """Get predictions for all available animals"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    animals = db.animals.find({'status': 'Available'})
    predictions = []
    
    for animal in animals:
        animal_doc = serialize_doc(animal)
        animal_id = animal_doc['_id']
        
        # Get medical history count
        try:
            medical_count = db.medical_records.count_documents({'animal_id': animal_id})
        except:
            medical_count = 0
        
        try:
            # Use simple rule-based priority score instead of ML
            priority_score, score_factors = calculate_priority_score(animal_doc, db)
            time_to_adoption, time_importance = predict_time_to_adoption(animal_doc, db)
            
            # Determine priority level based on score
            priority = 'Low'
            if priority_score:
                if priority_score >= 0.7:
                    priority = 'High'
                elif priority_score >= 0.4:
                    priority = 'Medium'
            
            predictions.append({
                '_id': animal_id,
                'name': animal_doc['name'],
                'species': animal_doc['species'],
                'breed': animal_doc.get('breed') or 'Unknown',
                'age': animal_doc.get('age', 0),
                'gender': animal_doc.get('gender', 'Unknown'),
                'medical_count': medical_count,
                'behavioral_notes': animal_doc.get('behavioral_notes') or 'N/A',
                'priority_score': round(priority_score * 100, 2) if priority_score else None,
                'time_to_adoption_days': round(time_to_adoption, 1) if time_to_adoption else None,
                'priority': priority,
                'score_factors': score_factors  # Show what factors contributed
            })
        except Exception as e:
            predictions.append({
                '_id': animal_id,
                'name': animal_doc['name'],
                'species': animal_doc['species'],
                'breed': animal_doc.get('breed') or 'Unknown',
                'age': animal_doc.get('age', 0),
                'gender': animal_doc.get('gender', 'Unknown'),
                'medical_count': medical_count,
                'behavioral_notes': animal_doc.get('behavioral_notes') or 'N/A',
                'priority_score': None,
                'time_to_adoption_days': None,
                'priority': 'Unknown',
                'error': str(e)
            })
    
    return predictions


@router.get("/feature-importance")
async def get_feature_importance():
    """Get feature importance from trained models"""
    import joblib
    
    importance = {}
    
    # Try to load feature importance from saved models
    try:
        if os.path.exists(ADOPTION_LIKELIHOOD_MODEL_PATH):
            model = joblib.load(ADOPTION_LIKELIHOOD_MODEL_PATH)
            feature_names = joblib.load(FEATURE_NAMES_PATH)
            feature_importance_dict = dict(zip(feature_names, model.feature_importances_))
            # Map encoded names back to readable names
            readable_names = {
                'species_encoded': 'species',
                'breed_encoded': 'breed',
                'age': 'age',
                'gender_encoded': 'gender',
                'status_encoded': 'status',
                'days_in_shelter': 'days_in_shelter',
                'medical_count': 'medical_count'
            }
            importance['adoption_likelihood'] = {
                readable_names.get(k, k): round(v, 4) 
                for k, v in feature_importance_dict.items()
            }
    except Exception as e:
        pass
    
    try:
        if os.path.exists(TIME_TO_ADOPTION_MODEL_PATH):
            model = joblib.load(TIME_TO_ADOPTION_MODEL_PATH)
            # For time model, features are: species, breed, age, gender, days_in_shelter, medical_count
            feature_names = ['species_encoded', 'breed_encoded', 'age', 'gender_encoded', 'days_in_shelter', 'medical_count']
            feature_importance_dict = dict(zip(feature_names, model.feature_importances_))
            readable_names = {
                'species_encoded': 'species',
                'breed_encoded': 'breed',
                'age': 'age',
                'gender_encoded': 'gender',
                'days_in_shelter': 'days_in_shelter',
                'medical_count': 'medical_count'
            }
            importance['time_to_adoption'] = {
                readable_names.get(k, k): round(v, 4) 
                for k, v in feature_importance_dict.items()
            }
    except Exception as e:
        pass
    
    if not importance:
        raise HTTPException(status_code=404, detail="Models not trained yet. Train models first.")
    
    return importance


@router.get("/model-status", response_model=Dict)
async def get_model_status():
    """Get status of trained models"""
    likelihood_exists = os.path.exists(ADOPTION_LIKELIHOOD_MODEL_PATH)
    time_exists = os.path.exists(TIME_TO_ADOPTION_MODEL_PATH)
    
    # Get file modification times if models exist
    likelihood_trained_date = None
    time_trained_date = None
    
    if likelihood_exists:
        likelihood_trained_date = os.path.getmtime(ADOPTION_LIKELIHOOD_MODEL_PATH)
    if time_exists:
        time_trained_date = os.path.getmtime(TIME_TO_ADOPTION_MODEL_PATH)
    
    return {
        'adoption_likelihood': {
            'trained': likelihood_exists,
            'trained_date': likelihood_trained_date
        },
        'time_to_adoption': {
            'trained': time_exists,
            'trained_date': time_trained_date
        }
    }


@router.get("/predict/animal/{animal_id}", response_model=Dict)
async def predict_animal(animal_id: str):
    """Get prediction for a specific animal"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        animal = db.animals.find_one({'_id': ObjectId(animal_id)})
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found")
        
        animal_doc = serialize_doc(animal)
        priority_score, _ = calculate_priority_score(animal_doc, db)
        time_to_adoption, _ = predict_time_to_adoption(animal_doc, db)
        
        return {
            'animal_id': animal_id,
            'priority_score': round(priority_score * 100, 2) if priority_score else None,
            'time_to_adoption_days': round(time_to_adoption, 1) if time_to_adoption else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")


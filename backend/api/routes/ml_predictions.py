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
from ml.models import train_all_models, predict_adoption_likelihood, predict_time_to_adoption

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def ml_predictions_page(request: Request):
    """Render ML predictions page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    animals_list = [serialize_doc(a) for a in db.animals.find({'status': 'Available'})]
    return templates.TemplateResponse("ml_predictions.html", {"request": request, "animals": animals_list})


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
        try:
            likelihood = predict_adoption_likelihood(animal_doc)
            time_to_adoption = predict_time_to_adoption(animal_doc)
            predictions.append({
                '_id': animal_doc['_id'],
                'name': animal_doc['name'],
                'species': animal_doc['species'],
                'adoption_likelihood': round(likelihood * 100, 2) if likelihood else None,
                'time_to_adoption_days': round(time_to_adoption, 1) if time_to_adoption else None
            })
        except:
            predictions.append({
                '_id': animal_doc['_id'],
                'name': animal_doc['name'],
                'species': animal_doc['species'],
                'adoption_likelihood': None,
                'time_to_adoption_days': None
            })
    
    return predictions


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
        likelihood = predict_adoption_likelihood(animal_doc)
        time_to_adoption = predict_time_to_adoption(animal_doc)
        
        return {
            'animal_id': animal_id,
            'adoption_likelihood': round(likelihood * 100, 2) if likelihood else None,
            'time_to_adoption_days': round(time_to_adoption, 1) if time_to_adoption else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")


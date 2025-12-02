"""
Search Routes
Search functionality for adoptions and medical records
"""

from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List, Dict

from backend.database.connection import get_database, serialize_doc

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/adopter", response_class=HTMLResponse, include_in_schema=False)
async def search_adopter_page(request: Request):
    """Render search by adopter page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't reach database")
    
    adopters_list = [serialize_doc(a) for a in db.adopters.find()]
    return templates.TemplateResponse("search_adopter.html", {"request": request, "adopters": adopters_list})


@router.get("/adopter/{adopter_id}", response_model=List[Dict])
async def search_by_adopter(adopter_id: str):
    """Find all animals adopted by a specific adopter"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't reach database")
    
    try:
        adoptions = db.adoptions.find({'adopter_id': adopter_id})
        animals_list = []
        for adoption in adoptions:
            animal = db.animals.find_one({'_id': ObjectId(adoption['animal_id'])})
            if animal:
                animal_doc = serialize_doc(animal)
                animal_doc['adoption_date'] = adoption.get('adoption_date', '')
                animals_list.append(animal_doc)
        return animals_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error searching: {str(e)}")


@router.get("/medical", response_class=HTMLResponse, include_in_schema=False)
async def search_medical_page(request: Request):
    """Render search medical records page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't reach database")
    
    animals_list = [serialize_doc(a) for a in db.animals.find()]
    return templates.TemplateResponse("search_medical.html", {"request": request, "animals": animals_list})


@router.get("/medical/{animal_id}", response_model=List[Dict])
async def search_medical_records(animal_id: str):
    """Get all medical records for a selected animal - sorted by visit date"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't reach database")
    
    try:
        # Fetch records sorted by date (newest first)
        records = db.medical_records.find({'animal_id': animal_id}).sort('visit_date', -1)
        records_list = [serialize_doc(r) for r in records]
        return records_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error searching: {str(e)}")


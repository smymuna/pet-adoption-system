"""
Animals Routes
CRUD operations for animals
"""

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List, Dict

from backend.database.connection import get_database, serialize_doc
from backend.models import AnimalCreate, AnimalUpdate, AnimalResponse, SuccessResponse
from backend.species_breeds import SPECIES_LIST, SPECIES_BREEDS, get_breeds_for_species

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def animals_page(request: Request):
    """Render animals management page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    animals_list = [serialize_doc(a) for a in db.animals.find()]
    return templates.TemplateResponse("animals.html", {
        "request": request, 
        "animals": animals_list,
        "species_list": SPECIES_LIST,
        "species_breeds": SPECIES_BREEDS
    })


@router.get("", response_model=List[AnimalResponse])
async def get_animals():
    """Get all animals (API endpoint)"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Filter out incomplete records (missing required fields)
    animals_list = []
    for a in db.animals.find():
        # Check if all required fields are present
        if all(key in a for key in ['name', 'species', 'age', 'gender', 'status']):
            animals_list.append(serialize_doc(a))
    return animals_list


@router.get("/species-breeds")
async def get_species_breeds():
    """Get species and breeds mapping"""
    return {"species_breeds": SPECIES_BREEDS, "species_list": SPECIES_LIST}


@router.post("", response_model=AnimalResponse)
async def create_animal(animal: AnimalCreate):
    """Create a new animal"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    animal_dict = animal.dict()
    result = db.animals.insert_one(animal_dict)
    created_animal = db.animals.find_one({'_id': result.inserted_id})
    return serialize_doc(created_animal)


@router.get("/{animal_id}", response_model=AnimalResponse)
async def get_animal(animal_id: str = Path(...)):
    """Get a specific animal by ID"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        animal_id_obj = ObjectId(animal_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid animal ID")
    
    animal = db.animals.find_one({'_id': animal_id_obj})
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return serialize_doc(animal)


@router.put("/{animal_id}", response_model=AnimalResponse)
async def update_animal(animal_id: str = Path(...), animal: AnimalUpdate = None):
    """Update an animal"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        animal_id_obj = ObjectId(animal_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid animal ID")
    
    update_data = {k: v for k, v in animal.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = db.animals.update_one({'_id': animal_id_obj}, {'$set': update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    updated_animal = db.animals.find_one({'_id': animal_id_obj})
    return serialize_doc(updated_animal)


@router.delete("/{animal_id}", response_model=SuccessResponse)
async def delete_animal(animal_id: str = Path(...)):
    """Delete an animal"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        animal_id_obj = ObjectId(animal_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid animal ID")
    
    result = db.animals.delete_one({'_id': animal_id_obj})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Animal not found")
    return SuccessResponse(success=True, message="Animal deleted successfully")


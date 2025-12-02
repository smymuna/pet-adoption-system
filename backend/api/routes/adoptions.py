"""
Adoptions Routes
CRUD operations for adoptions
"""

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List
from datetime import datetime

from backend.database.connection import get_database, serialize_doc
from backend.models import AdoptionCreate, AdoptionUpdate, AdoptionResponse, SuccessResponse

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def adoptions_page(request: Request):
    """Render adoptions management page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't connect to database")
    
    adoptions_list = []
    for adoption in db.adoptions.find():
        adoption_doc = serialize_doc(adoption)
        # Get animal and adopter details
        animal = db.animals.find_one({'_id': ObjectId(adoption['animal_id'])})
        adopter = db.adopters.find_one({'_id': ObjectId(adoption['adopter_id'])})
        adoption_doc['animal_name'] = animal['name'] if animal else 'Unknown'
        adoption_doc['adopter_name'] = adopter['name'] if adopter else 'Unknown'
        adoptions_list.append(adoption_doc)
    
    return templates.TemplateResponse("adoptions.html", {"request": request, "adoptions": adoptions_list})


@router.get("", response_model=List[AdoptionResponse])
async def get_adoptions():
    """Get all adoptions"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't connect to database")
    
    adoptions_list = [serialize_doc(a) for a in db.adoptions.find()]
    return adoptions_list


@router.post("", response_model=AdoptionResponse)
async def create_adoption(adoption: AdoptionCreate):
    """Create a new adoption - automatically updates animal status to 'Adopted'"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't connect to database")
    
    # Validate IDs and check existence
    try:
        animal_id_obj = ObjectId(adoption.animal_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid animal ID format")
    
    animal = db.animals.find_one({'_id': animal_id_obj})
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    try:
        adopter_id_obj = ObjectId(adoption.adopter_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid adopter ID format")
    
    adopter = db.adopters.find_one({'_id': adopter_id_obj})
    if not adopter:
        raise HTTPException(status_code=404, detail="Adopter not found")
    
    adoption_dict = adoption.dict()
    # Default to today if no date provided
    if not adoption_dict.get('adoption_date'):
        adoption_dict['adoption_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Mark animal as adopted
    db.animals.update_one({'_id': animal_id_obj}, {'$set': {'status': 'Adopted'}})
    
    result = db.adoptions.insert_one(adoption_dict)
    adoption_dict['_id'] = str(result.inserted_id)
    return adoption_dict


@router.get("/{adoption_id}", response_model=AdoptionResponse)
async def get_adoption(adoption_id: str = Path(...)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't connect to database")
    
    try:
        adoption = db.adoptions.find_one({'_id': ObjectId(adoption_id)})
        if not adoption:
            raise HTTPException(status_code=404, detail="Adoption not found")
        return serialize_doc(adoption)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad adoption ID")


@router.put("/{adoption_id}", response_model=AdoptionResponse)
async def update_adoption(adoption_id: str = Path(...), adoption: AdoptionUpdate = None):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't connect to database")
    
    try:
        update_data = {k: v for k, v in adoption.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.adoptions.update_one({'_id': ObjectId(adoption_id)}, {'$set': update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Adoption not found")
        
        updated_adoption = db.adoptions.find_one({'_id': ObjectId(adoption_id)})
        return serialize_doc(updated_adoption)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid adoption ID")


@router.delete("/{adoption_id}", response_model=SuccessResponse)
async def delete_adoption(adoption_id: str = Path(...)):
    """Delete an adoption"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't connect to database")
    
    try:
        adoption = db.adoptions.find_one({'_id': ObjectId(adoption_id)})
        if not adoption:
            raise HTTPException(status_code=404, detail="Adoption not found")
        
        # Update animal status back to Available
        animal_id = adoption.get('animal_id')
        if animal_id:
            if isinstance(animal_id, str):
                animal_id = ObjectId(animal_id)
            db.animals.update_one({'_id': animal_id}, {'$set': {'status': 'Available'}})
        
        result = db.adoptions.delete_one({'_id': ObjectId(adoption_id)})
        return SuccessResponse(success=True, message="Adoption deleted successfully")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid adoption ID")


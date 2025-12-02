"""
Adopters Routes
CRUD operations for adopters
"""

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List

from backend.database.connection import get_database, serialize_doc
from backend.models import AdopterCreate, AdopterUpdate, AdopterResponse, SuccessResponse

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def adopters_page(request: Request):
    """Render adopters management page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB connection error")
    
    adopters_list = [serialize_doc(a) for a in db.adopters.find()]
    return templates.TemplateResponse("adopters.html", {"request": request, "adopters": adopters_list})


@router.get("", response_model=List[AdopterResponse])
async def get_adopters():
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Could not connect to database")
    
    # Fetch all adopters - simple list comprehension works fine here
    adopters_list = [serialize_doc(a) for a in db.adopters.find()]
    return adopters_list


@router.post("", response_model=AdopterResponse)
async def create_adopter(adopter: AdopterCreate):
    # Add new adopter to database
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    # Convert to dict and insert
    adopter_dict = adopter.dict()
    result = db.adopters.insert_one(adopter_dict)
    adopter_dict['_id'] = str(result.inserted_id)
    return adopter_dict


@router.get("/{adopter_id}", response_model=AdopterResponse)
async def get_adopter(adopter_id: str = Path(...)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    try:
        adopter_obj_id = ObjectId(adopter_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad ID format")
    
    adopter = db.adopters.find_one({'_id': adopter_obj_id})
    if not adopter:
        raise HTTPException(status_code=404, detail="Adopter doesn't exist")
    
    return serialize_doc(adopter)


@router.put("/{adopter_id}", response_model=AdopterResponse)
async def update_adopter(adopter_id: str = Path(...), adopter: AdopterUpdate = None):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    try:
        update_data = {k: v for k, v in adopter.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.adopters.update_one({'_id': ObjectId(adopter_id)}, {'$set': update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Adopter not found")
        
        updated_adopter = db.adopters.find_one({'_id': ObjectId(adopter_id)})
        return serialize_doc(updated_adopter)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid adopter ID")


@router.delete("/{adopter_id}", response_model=SuccessResponse)
async def delete_adopter(adopter_id: str = Path(...)):
    # TODO: consider soft delete instead of hard delete
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    try:
        result = db.adopters.delete_one({'_id': ObjectId(adopter_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Adopter not found")
        return SuccessResponse(success=True, message="Adopter deleted successfully")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid adopter ID")


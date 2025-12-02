"""
Volunteers Routes
CRUD operations for volunteers
"""

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List

from backend.database.connection import get_database, serialize_doc
from backend.models import VolunteerCreate, VolunteerUpdate, VolunteerResponse, SuccessResponse
from backend.volunteer_skills import VOLUNTEER_SKILLS

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def volunteers_page(request: Request):
    """Render volunteers management page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    volunteers_list = []
    for v in db.volunteers.find():
        volunteer_doc = serialize_doc(v)
        # Convert skills to list if it's a string (backward compatibility)
        if isinstance(volunteer_doc.get('skills'), str):
            volunteer_doc['skills'] = [volunteer_doc['skills']]
        elif volunteer_doc.get('skills') is None:
            volunteer_doc['skills'] = []
        volunteers_list.append(volunteer_doc)
    
    return templates.TemplateResponse("volunteers.html", {
        "request": request, 
        "volunteers": volunteers_list,
        "volunteer_skills": VOLUNTEER_SKILLS
    })


@router.get("", response_model=List[VolunteerResponse])
async def get_volunteers():
    """Get all volunteers - handles legacy string skills format"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    volunteers_list = []
    for v in db.volunteers.find():
        volunteer_doc = serialize_doc(v)
        # Handle old data where skills was stored as string instead of list
        if isinstance(volunteer_doc.get('skills'), str):
            volunteer_doc['skills'] = [volunteer_doc['skills']]
        elif volunteer_doc.get('skills') is None:
            volunteer_doc['skills'] = []
        volunteers_list.append(volunteer_doc)
    return volunteers_list


@router.post("", response_model=VolunteerResponse)
async def create_volunteer(volunteer: VolunteerCreate):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    volunteer_dict = volunteer.dict()
    result = db.volunteers.insert_one(volunteer_dict)
    volunteer_dict['_id'] = str(result.inserted_id)
    return volunteer_dict


@router.get("/{volunteer_id}", response_model=VolunteerResponse)
async def get_volunteer(volunteer_id: str = Path(...)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    try:
        volunteer = db.volunteers.find_one({'_id': ObjectId(volunteer_id)})
        if not volunteer:
            raise HTTPException(status_code=404, detail="Volunteer not found")
        return serialize_doc(volunteer)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad volunteer ID")


@router.put("/{volunteer_id}", response_model=VolunteerResponse)
async def update_volunteer(volunteer_id: str = Path(...), volunteer: VolunteerUpdate = None):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    try:
        update_data = {k: v for k, v in volunteer.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.volunteers.update_one({'_id': ObjectId(volunteer_id)}, {'$set': update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Volunteer not found")
        
        updated_volunteer = db.volunteers.find_one({'_id': ObjectId(volunteer_id)})
        return serialize_doc(updated_volunteer)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid volunteer ID")


@router.delete("/{volunteer_id}", response_model=SuccessResponse)
async def delete_volunteer(volunteer_id: str = Path(...)):
    """Delete a volunteer"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    try:
        result = db.volunteers.delete_one({'_id': ObjectId(volunteer_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Volunteer not found")
        return SuccessResponse(success=True, message="Volunteer deleted successfully")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid volunteer ID")


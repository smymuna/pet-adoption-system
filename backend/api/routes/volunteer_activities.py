"""
Volunteer Activities Routes
CRUD operations for volunteer activities
"""

from fastapi import APIRouter, Request, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

from backend.database.connection import get_database, serialize_doc
from backend.models import (
    VolunteerActivityCreate, 
    VolunteerActivityUpdate, 
    VolunteerActivityResponse, 
    SuccessResponse
)

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Activity types
ACTIVITY_TYPES = [
    "Walking",
    "Feeding",
    "Grooming",
    "Training",
    "Socialization",
    "Medical Assistance",
    "Adoption Event",
    "Meet & Greet",
    "Cleaning",
    "Transportation",
    "Other"
]


@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def volunteer_activities_page(request: Request):
    """Render volunteer activities management page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    activities_list = []
    for activity in db.volunteer_activities.find().sort("activity_date", -1):
        activity_doc = serialize_doc(activity)
        # Get volunteer and animal names
        try:
            volunteer = db.volunteers.find_one({'_id': ObjectId(activity['volunteer_id'])})
            animal = db.animals.find_one({'_id': ObjectId(activity['animal_id'])})
            activity_doc['volunteer_name'] = volunteer.get('name', 'Unknown') if volunteer else 'Unknown'
            activity_doc['animal_name'] = animal.get('name', 'Unknown') if animal else 'Unknown'
        except Exception:
            activity_doc['volunteer_name'] = 'Unknown'
            activity_doc['animal_name'] = 'Unknown'
        activities_list.append(activity_doc)
    
    volunteers_list = [serialize_doc(v) for v in db.volunteers.find()]
    animals_list = [serialize_doc(a) for a in db.animals.find()]
    
    return templates.TemplateResponse("volunteer_activities.html", {
        "request": request,
        "activities": activities_list,
        "volunteers": volunteers_list,
        "animals": animals_list,
        "activity_types": ACTIVITY_TYPES
    })


@router.get("", response_model=List[VolunteerActivityResponse])
async def get_volunteer_activities(
    volunteer_id: Optional[str] = Query(None, description="Filter by volunteer ID"),
    animal_id: Optional[str] = Query(None, description="Filter by animal ID")
):
    """Get all volunteer activities with optional filters"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    filter_dict = {}
    if volunteer_id:
        filter_dict['volunteer_id'] = volunteer_id
    if animal_id:
        filter_dict['animal_id'] = animal_id
    
    activities = [serialize_doc(a) for a in db.volunteer_activities.find(filter_dict).sort("activity_date", -1)]
    return activities


@router.post("", response_model=VolunteerActivityResponse)
async def create_volunteer_activity(activity: VolunteerActivityCreate):
    """Create a new volunteer activity"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    # Validate IDs first, then check existence
    try:
        volunteer_id_obj = ObjectId(activity.volunteer_id)
        animal_id_obj = ObjectId(activity.animal_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    # Check both exist in database
    volunteer = db.volunteers.find_one({'_id': volunteer_id_obj})
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    animal = db.animals.find_one({'_id': animal_id_obj})
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    activity_dict = activity.dict()
    result = db.volunteer_activities.insert_one(activity_dict)
    activity_dict['_id'] = str(result.inserted_id)
    return activity_dict


@router.get("/{activity_id}", response_model=VolunteerActivityResponse)
async def get_volunteer_activity(activity_id: str = Path(...)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    try:
        activity = db.volunteer_activities.find_one({'_id': ObjectId(activity_id)})
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return serialize_doc(activity)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid activity ID")


@router.put("/{activity_id}", response_model=VolunteerActivityResponse)
async def update_volunteer_activity(activity_id: str = Path(...), activity: VolunteerActivityUpdate = None):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    try:
        update_data = {k: v for k, v in activity.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.volunteer_activities.update_one({'_id': ObjectId(activity_id)}, {'$set': update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        updated_activity = db.volunteer_activities.find_one({'_id': ObjectId(activity_id)})
        return serialize_doc(updated_activity)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid activity ID")


@router.delete("/{activity_id}", response_model=SuccessResponse)
async def delete_volunteer_activity(activity_id: str = Path(...)):
    # Allow deletion but might want to keep for reporting later
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    try:
        result = db.volunteer_activities.delete_one({'_id': ObjectId(activity_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Activity not found")
        return SuccessResponse(success=True, message="Activity deleted successfully")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid activity ID")


@router.get("/stats/summary", response_model=dict)
async def get_volunteer_stats():
    """Get volunteer statistics"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    activities = list(db.volunteer_activities.find())
    
    total_hours = sum(a.get('duration_minutes', 0) for a in activities) / 60
    total_activities = len(activities)
    
    # Activities by type
    activities_by_type = {}
    for activity in activities:
        activity_type = activity.get('activity_type', 'Other')
        activities_by_type[activity_type] = activities_by_type.get(activity_type, 0) + 1
    
    # Top volunteers by hours
    volunteer_hours = {}
    for activity in activities:
        volunteer_id = activity.get('volunteer_id')
        if volunteer_id:
            minutes = activity.get('duration_minutes', 0)
            volunteer_hours[volunteer_id] = volunteer_hours.get(volunteer_id, 0) + minutes
    
    top_volunteers = sorted(volunteer_hours.items(), key=lambda x: x[1], reverse=True)[:5]
    top_volunteers_list = []
    for volunteer_id, minutes in top_volunteers:
        try:
            volunteer = db.volunteers.find_one({'_id': ObjectId(volunteer_id)})
            if volunteer:
                top_volunteers_list.append({
                    'name': volunteer.get('name', 'Unknown'),
                    'hours': round(minutes / 60, 1)
                })
        except Exception:
            continue
    
    return {
        'total_hours': round(total_hours, 1),
        'total_activities': total_activities,
        'activities_by_type': activities_by_type,
        'top_volunteers': top_volunteers_list
    }


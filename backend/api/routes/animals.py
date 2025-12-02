"""
Animals Routes
CRUD operations for animals
"""

from fastapi import APIRouter, Request, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List, Dict, Optional

from backend.database.connection import get_database, serialize_doc
from backend.models import (
    AnimalCreate, AnimalUpdate, AnimalResponse, SuccessResponse,
    VolunteerAssignmentCreate, VolunteerAssignmentResponse
)
from backend.species_breeds import SPECIES_LIST, SPECIES_BREEDS, get_breeds_for_species
from backend.volunteer_skills import get_skills_for_species

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def animals_page(request: Request, status: Optional[str] = None):
    """Render animals management page with optional status filter"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Validate status parameter
    valid_statuses = ["Available", "Adopted", "Medical"]
    if status and status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    
    # Build filter based on query parameters
    filter_dict = {}
    if status:
        filter_dict['status'] = status
    
    animals_list = []
    volunteers_list = [serialize_doc(v) for v in db.volunteers.find()]
    
    for animal in db.animals.find(filter_dict):
        animal_doc = serialize_doc(animal)
        # Populate volunteer names and IDs if assigned
        if animal_doc.get('assigned_volunteers'):
            volunteer_info = []
            for vol_id in animal_doc['assigned_volunteers']:
                try:
                    volunteer = db.volunteers.find_one({'_id': ObjectId(vol_id)})
                    if volunteer:
                        volunteer_info.append({
                            'id': vol_id,
                            'name': volunteer.get('name', 'Unknown')
                        })
                except Exception:
                    continue
            animal_doc['assigned_volunteer_info'] = volunteer_info
            # Keep backward compatibility
            animal_doc['assigned_volunteer_names'] = [v['name'] for v in volunteer_info]
        animals_list.append(animal_doc)
    
    return templates.TemplateResponse("animals.html", {
        "request": request, 
        "animals": animals_list,
        "species_list": SPECIES_LIST,
        "species_breeds": SPECIES_BREEDS,
        "initial_status_filter": status,
        "volunteers": volunteers_list
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


@router.post("/{animal_id}/assign-volunteer", response_model=VolunteerAssignmentResponse)
async def assign_volunteer_to_animal(animal_id: str = Path(...), assignment: VolunteerAssignmentCreate = None):
    """Assign a volunteer to an animal"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        animal_id_obj = ObjectId(animal_id)
        volunteer_id_obj = ObjectId(assignment.volunteer_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid animal or volunteer ID")
    
    # Verify animal and volunteer exist
    animal = db.animals.find_one({'_id': animal_id_obj})
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    volunteer = db.volunteers.find_one({'_id': volunteer_id_obj})
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    # Get current assigned volunteers or initialize empty list
    assigned_volunteers = animal.get('assigned_volunteers', [])
    volunteer_id_str = str(volunteer_id_obj)
    
    # Check if already assigned
    if volunteer_id_str in assigned_volunteers:
        raise HTTPException(status_code=400, detail="Volunteer is already assigned to this animal")
    
    # Add volunteer to assigned list
    assigned_volunteers.append(volunteer_id_str)
    db.animals.update_one({'_id': animal_id_obj}, {'$set': {'assigned_volunteers': assigned_volunteers}})
    
    return VolunteerAssignmentResponse(
        success=True,
        message=f"Volunteer {volunteer.get('name', 'Unknown')} assigned to {animal.get('name', 'Unknown')}",
        animal_id=animal_id,
        volunteer_id=assignment.volunteer_id
    )


@router.delete("/{animal_id}/unassign-volunteer/{volunteer_id}", response_model=SuccessResponse)
async def unassign_volunteer_from_animal(animal_id: str = Path(...), volunteer_id: str = Path(...)):
    """Unassign a volunteer from an animal"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        animal_id_obj = ObjectId(animal_id)
        volunteer_id_obj = ObjectId(volunteer_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid animal or volunteer ID")
    
    animal = db.animals.find_one({'_id': animal_id_obj})
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    assigned_volunteers = animal.get('assigned_volunteers', [])
    volunteer_id_str = str(volunteer_id_obj)
    
    if volunteer_id_str not in assigned_volunteers:
        raise HTTPException(status_code=400, detail="Volunteer is not assigned to this animal")
    
    # Remove volunteer from assigned list
    assigned_volunteers.remove(volunteer_id_str)
    db.animals.update_one({'_id': animal_id_obj}, {'$set': {'assigned_volunteers': assigned_volunteers}})
    
    return SuccessResponse(success=True, message="Volunteer unassigned successfully")


@router.get("/{animal_id}/suggested-volunteers", response_model=dict)
async def get_suggested_volunteers(animal_id: str = Path(...)):
    """Get suggested volunteers for an animal based on skills and species"""
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
    
    species = animal.get('species', '')
    relevant_skills = get_skills_for_species(species)
    
    # Find volunteers with matching skills
    all_volunteers = list(db.volunteers.find())
    suggested = []
    
    for volunteer in all_volunteers:
        volunteer_skills = volunteer.get('skills', [])
        if isinstance(volunteer_skills, str):
            volunteer_skills = [volunteer_skills]  # Handle old format
        
        # Count matching skills
        matching_skills = [skill for skill in volunteer_skills if skill in relevant_skills]
        if matching_skills:
            suggested.append({
                'id': str(volunteer['_id']),
                'name': volunteer.get('name', 'Unknown'),
                'skills': volunteer_skills,
                'matching_skills': matching_skills,
                'match_score': len(matching_skills)
            })
    
    # Sort by match score
    suggested.sort(key=lambda x: x['match_score'], reverse=True)
    
    return {
        'animal_id': animal_id,
        'animal_name': animal.get('name', 'Unknown'),
        'species': species,
        'relevant_skills': relevant_skills,
        'suggested_volunteers': suggested
    }


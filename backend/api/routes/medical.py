"""
Medical Records Routes
CRUD operations for medical records
"""

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from typing import List

from backend.database.connection import get_database, serialize_doc
from backend.models import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse, SuccessResponse

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def medical_page(request: Request):
    """Render medical records management page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    records_list = []
    # Loop through records and enrich with animal names for display
    for record in db.medical_records.find():
        record_doc = serialize_doc(record)
        try:
            animal = db.animals.find_one({'_id': ObjectId(record['animal_id'])})
            record_doc['animal_name'] = animal.get('name', 'Unknown') if animal else 'Unknown'
        except (KeyError, TypeError):
            record_doc['animal_name'] = 'Unknown'
        records_list.append(record_doc)
    
    return templates.TemplateResponse("medical.html", {"request": request, "records": records_list})


@router.get("", response_model=List[MedicalRecordResponse])
async def get_medical_records():
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    records_list = [serialize_doc(r) for r in db.medical_records.find()]
    return records_list


@router.post("", response_model=MedicalRecordResponse)
async def create_medical_record(record: MedicalRecordCreate):
    """Create a new medical record - validates animal exists first"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    # Make sure the animal actually exists before creating record
    try:
        animal_id_obj = ObjectId(record.animal_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid animal ID format")
    
    animal = db.animals.find_one({'_id': animal_id_obj})
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    record_dict = record.dict()
    result = db.medical_records.insert_one(record_dict)
    record_dict['_id'] = str(result.inserted_id)
    return record_dict


@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_medical_record(record_id: str = Path(...)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    try:
        record = db.medical_records.find_one({'_id': ObjectId(record_id)})
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return serialize_doc(record)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid record ID")


@router.put("/{record_id}", response_model=MedicalRecordResponse)
async def update_medical_record(record_id: str = Path(...), record: MedicalRecordUpdate = None):
    # Update existing medical record
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    try:
        update_data = {k: v for k, v in record.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = db.medical_records.update_one({'_id': ObjectId(record_id)}, {'$set': update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Medical record not found")
        
        updated_record = db.medical_records.find_one({'_id': ObjectId(record_id)})
        return serialize_doc(updated_record)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid medical record ID")


@router.delete("/{record_id}", response_model=SuccessResponse)
async def delete_medical_record(record_id: str = Path(...)):
    # Note: medical records should probably be kept for history, but allowing delete for now
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    try:
        result = db.medical_records.delete_one({'_id': ObjectId(record_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Medical record not found")
        return SuccessResponse(success=True, message="Medical record deleted successfully")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid medical record ID")


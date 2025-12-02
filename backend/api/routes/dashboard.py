"""
Dashboard Routes
Main dashboard page with statistics
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.database.connection import get_database

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Render dashboard page with statistics"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Calculate volunteer statistics
    total_activities = db.volunteer_activities.count_documents({})
    total_hours = 0
    animals_needing_volunteers = 0
    
    # Calculate total volunteer hours
    for activity in db.volunteer_activities.find():
        total_hours += activity.get('duration_minutes', 0) / 60
    
    # Count animals without assigned volunteers
    for animal in db.animals.find({'status': 'Available'}):
        assigned = animal.get('assigned_volunteers', [])
        if not assigned or len(assigned) == 0:
            animals_needing_volunteers += 1
    
    stats = {
        'total_animals': db.animals.count_documents({}),
        'total_adopters': db.adopters.count_documents({}),
        'total_adoptions': db.adoptions.count_documents({}),
        'total_volunteers': db.volunteers.count_documents({}),
        'available_animals': db.animals.count_documents({'status': 'Available'}),
        'adopted_animals': db.animals.count_documents({'status': 'Adopted'}),
        'total_volunteer_hours': round(total_hours, 1),
        'total_volunteer_activities': total_activities,
        'animals_needing_volunteers': animals_needing_volunteers
    }
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "stats": stats})


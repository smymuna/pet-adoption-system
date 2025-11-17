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
    
    stats = {
        'total_animals': db.animals.count_documents({}),
        'total_adopters': db.adopters.count_documents({}),
        'total_adoptions': db.adoptions.count_documents({}),
        'total_volunteers': db.volunteers.count_documents({}),
        'available_animals': db.animals.count_documents({'status': 'Available'}),
        'adopted_animals': db.animals.count_documents({'status': 'Adopted'})
    }
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "stats": stats})


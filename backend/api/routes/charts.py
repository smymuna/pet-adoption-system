"""
Charts Routes
Data visualization endpoints
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from collections import Counter
from datetime import datetime

from backend.database.connection import get_database

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def charts_page(request: Request):
    """Render charts page"""
    return templates.TemplateResponse("charts.html", {"request": request})


@router.get("/species", response_model=Dict)
async def get_species_distribution():
    """Get animal species distribution for pie/bar chart"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    animals = db.animals.find()
    # Filter out animals without species field and handle missing data
    species_count = Counter(
        animal.get('species', 'Unknown') 
        for animal in animals 
        if animal.get('species') is not None
    )
    
    return {
        'labels': list(species_count.keys()),
        'data': list(species_count.values())
    }


@router.get("/adoptions", response_model=Dict)
async def get_monthly_adoptions():
    """Get monthly adoption numbers for line chart"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    adoptions = db.adoptions.find()
    monthly_count = Counter()
    
    for adoption in adoptions:
        adoption_date = adoption.get('adoption_date', '')
        if adoption_date:
            try:
                # Parse date and extract year-month
                date_obj = datetime.strptime(adoption_date, '%Y-%m-%d')
                month_key = date_obj.strftime('%Y-%m')
                monthly_count[month_key] += 1
            except:
                pass
    
    # Sort by month
    sorted_months = sorted(monthly_count.items())
    
    return {
        'labels': [item[0] for item in sorted_months],
        'data': [item[1] for item in sorted_months]
    }


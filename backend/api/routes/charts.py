"""
Charts Routes
Data visualization endpoints with filtering support
"""

from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Optional
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from bson import ObjectId

from backend.database.connection import get_database

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def charts_page(request: Request):
    """Render charts page"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Get filter options
    species_list = sorted(set(a.get('species', '') for a in db.animals.find() if a.get('species')))
    status_list = sorted(set(a.get('status', '') for a in db.animals.find() if a.get('status')))
    gender_list = sorted(set(a.get('gender', '') for a in db.animals.find() if a.get('gender')))
    
    return templates.TemplateResponse("charts.html", {
        "request": request,
        "species_list": species_list,
        "status_list": status_list,
        "gender_list": gender_list
    })


def build_animal_filter(species: Optional[str] = None, status: Optional[str] = None, 
                       gender: Optional[str] = None, start_date: Optional[str] = None,
                       end_date: Optional[str] = None):
    """Build MongoDB filter for animals based on query parameters"""
    filter_dict = {}
    
    if species:
        filter_dict['species'] = species
    if status:
        filter_dict['status'] = status
    if gender:
        filter_dict['gender'] = gender
    
    # Date filtering would require an intake_date field, which we don't have
    # For now, we'll skip date filtering on animals directly
    
    return filter_dict


@router.get("/species", response_model=Dict)
async def get_species_distribution(
    status: Optional[str] = Query(None, description="Filter by animal status"),
    gender: Optional[str] = Query(None, description="Filter by gender")
):
    """Get animal species distribution with optional filters"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = {}
    if status:
        filter_dict['status'] = status
    if gender:
        filter_dict['gender'] = gender
    
    animals = db.animals.find(filter_dict)
    species_count = Counter(
        animal.get('species', 'Unknown') 
        for animal in animals 
        if animal.get('species') is not None
    )
    
    # Sort by count descending
    sorted_species = sorted(species_count.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'labels': [item[0] for item in sorted_species],
        'data': [item[1] for item in sorted_species]
    }


@router.get("/status", response_model=Dict)
async def get_status_distribution(
    species: Optional[str] = Query(None, description="Filter by species"),
    gender: Optional[str] = Query(None, description="Filter by gender")
):
    """Get animal status distribution (Available, Adopted, Medical)"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = {}
    if species:
        filter_dict['species'] = species
    if gender:
        filter_dict['gender'] = gender
    
    animals = db.animals.find(filter_dict)
    status_count = Counter(
        animal.get('status', 'Unknown') 
        for animal in animals 
        if animal.get('status') is not None
    )
    
    return {
        'labels': list(status_count.keys()),
        'data': list(status_count.values())
    }


@router.get("/age-distribution", response_model=Dict)
async def get_age_distribution(
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Get age distribution grouped into ranges"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = {}
    if species:
        filter_dict['species'] = species
    if status:
        filter_dict['status'] = status
    
    animals = db.animals.find(filter_dict)
    
    age_ranges = {
        '0-1 years': 0,
        '1-3 years': 0,
        '3-5 years': 0,
        '5-10 years': 0,
        '10+ years': 0
    }
    
    for animal in animals:
        age = animal.get('age', 0)
        if age <= 1:
            age_ranges['0-1 years'] += 1
        elif age <= 3:
            age_ranges['1-3 years'] += 1
        elif age <= 5:
            age_ranges['3-5 years'] += 1
        elif age <= 10:
            age_ranges['5-10 years'] += 1
        else:
            age_ranges['10+ years'] += 1
    
    return {
        'labels': list(age_ranges.keys()),
        'data': list(age_ranges.values())
    }


@router.get("/adoptions", response_model=Dict)
async def get_monthly_adoptions(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get monthly adoption numbers with optional date range filter"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    adoptions = db.adoptions.find()
    monthly_count = Counter()
    
    start_dt = None
    end_dt = None
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        except:
            pass
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except:
            pass
    
    for adoption in adoptions:
        adoption_date = adoption.get('adoption_date', '')
        if adoption_date:
            try:
                date_obj = datetime.strptime(adoption_date, '%Y-%m-%d')
                
                # Apply date filters
                if start_dt and date_obj < start_dt:
                    continue
                if end_dt and date_obj > end_dt:
                    continue
                
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


@router.get("/adoption-rate", response_model=Dict)
async def get_adoption_rate_by_species():
    """Get adoption rate (adopted vs available) by species"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    animals = db.animals.find()
    adoptions = db.adoptions.find()
    
    # Get all adopted animal IDs
    adopted_ids = {str(ad['animal_id']) for ad in adoptions}
    
    # Count by species
    species_stats = defaultdict(lambda: {'total': 0, 'adopted': 0})
    
    for animal in animals:
        species = animal.get('species', 'Unknown')
        animal_id = str(animal['_id'])
        species_stats[species]['total'] += 1
        if animal_id in adopted_ids:
            species_stats[species]['adopted'] += 1
    
    # Calculate adoption rates
    labels = []
    adopted_data = []
    available_data = []
    
    for species, stats in sorted(species_stats.items()):
        labels.append(species)
        adopted_data.append(stats['adopted'])
        available_data.append(stats['total'] - stats['adopted'])
    
    return {
        'labels': labels,
        'adopted': adopted_data,
        'available': available_data
    }


@router.get("/gender-distribution", response_model=Dict)
async def get_gender_distribution(
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Get gender distribution"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = {}
    if species:
        filter_dict['species'] = species
    if status:
        filter_dict['status'] = status
    
    animals = db.animals.find(filter_dict)
    gender_count = Counter(
        animal.get('gender', 'Unknown') 
        for animal in animals 
        if animal.get('gender') is not None
    )
    
    return {
        'labels': list(gender_count.keys()),
        'data': list(gender_count.values())
    }


@router.get("/medical-visits", response_model=Dict)
async def get_medical_visits(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get medical visits over time"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    medical_records = db.medical_records.find()
    monthly_count = Counter()
    
    start_dt = None
    end_dt = None
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        except:
            pass
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except:
            pass
    
    for record in medical_records:
        visit_date = record.get('visit_date', '')
        if visit_date:
            try:
                date_obj = datetime.strptime(visit_date, '%Y-%m-%d')
                
                # Apply date filters
                if start_dt and date_obj < start_dt:
                    continue
                if end_dt and date_obj > end_dt:
                    continue
                
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


"""
Charts Routes
Data visualization endpoints with filtering support
"""

from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Optional
from collections import Counter, defaultdict
from datetime import datetime

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
                       gender: Optional[str] = None):
    """Build MongoDB filter for animals based on query parameters"""
    filter_dict = {}
    
    if species:
        filter_dict['species'] = species
    if status:
        filter_dict['status'] = status
    if gender:
        filter_dict['gender'] = gender
    
    return filter_dict


def parse_date_range(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Parse and validate date range filters
    
    Returns:
        tuple: (start_dt, end_dt, metadata_dict) where dates are datetime objects or None
    """
    start_dt = None
    end_dt = None
    metadata = {
        'start_date': start_date,
        'end_date': end_date
    }
    
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            metadata['start_date_error'] = f"Invalid start_date format: {start_date}"
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            metadata['end_date_error'] = f"Invalid end_date format: {end_date}"
    
    # Validate date range
    if start_dt and end_dt and start_dt > end_dt:
        metadata['range_error'] = "start_date must be before or equal to end_date"
    
    return start_dt, end_dt, metadata


@router.get("/species", response_model=Dict)
async def get_species_distribution(
    species: Optional[str] = Query(None, description="Filter by species (for consistency)"),
    status: Optional[str] = Query(None, description="Filter by animal status"),
    gender: Optional[str] = Query(None, description="Filter by gender")
):
    """Get animal species distribution with optional filters"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender)
    
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
    status: Optional[str] = Query(None, description="Filter by status (for consistency)"),
    gender: Optional[str] = Query(None, description="Filter by gender")
):
    """Get animal status distribution (Available, Adopted, Medical)"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender)
    
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
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender")
):
    """Get age distribution grouped into ranges"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender)
    
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
    """Get monthly adoption numbers with optional date range filter
    
    Parameters:
    - start_date: Optional start date filter (YYYY-MM-DD format)
    - end_date: Optional end date filter (YYYY-MM-DD format)
    
    Returns monthly adoption counts grouped by year-month (YYYY-MM format)
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    adoptions = list(db.adoptions.find())
    monthly_count = Counter()
    
    start_dt, end_dt, date_metadata = parse_date_range(start_date, end_date)
    
    valid_dates = 0
    invalid_dates = 0
    
    for adoption in adoptions:
        adoption_date = adoption.get('adoption_date', '')
        if adoption_date:
            try:
                # Try parsing the date
                date_obj = datetime.strptime(str(adoption_date), '%Y-%m-%d')
                valid_dates += 1
                
                # Apply date filters
                if start_dt and date_obj < start_dt:
                    continue
                if end_dt and date_obj > end_dt:
                    continue
                
                month_key = date_obj.strftime('%Y-%m')
                monthly_count[month_key] += 1
            except (ValueError, TypeError) as e:
                invalid_dates += 1
                # Log for debugging
                print(f"Invalid adoption_date format: {adoption_date}, error: {e}")
    
    # Sort by month
    sorted_months = sorted(monthly_count.items())
    
    metadata = {
        'total_adoptions': len(adoptions),
        'valid_dates': valid_dates,
        'invalid_dates': invalid_dates,
        'filtered_count': sum(monthly_count.values()),
        **date_metadata
    }
    
    return {
        'labels': [item[0] for item in sorted_months],
        'data': [item[1] for item in sorted_months],
        'metadata': metadata
    }


@router.get("/adoption-rate", response_model=Dict)
async def get_adoption_rate_by_species(
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender")
):
    """Get adoption rate (adopted vs available) by species with optional filters"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Apply filters to animals
    filter_dict = build_animal_filter(species=species, status=status, gender=gender)
    animals = db.animals.find(filter_dict)
    adoptions = db.adoptions.find()
    
    # Get all adopted animal IDs
    adopted_ids = {str(ad['animal_id']) for ad in adoptions}
    
    # Count by species
    species_stats = defaultdict(lambda: {'total': 0, 'adopted': 0})
    
    for animal in animals:
        species_name = animal.get('species', 'Unknown')
        animal_id = str(animal['_id'])
        species_stats[species_name]['total'] += 1
        if animal_id in adopted_ids:
            species_stats[species_name]['adopted'] += 1
    
    # Calculate adoption rates
    labels = []
    adopted_data = []
    available_data = []
    
    for species_name, stats in sorted(species_stats.items()):
        labels.append(species_name)
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
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender (for consistency)")
):
    """Get gender distribution"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender)
    
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
    """Get medical visits over time
    
    Parameters:
    - start_date: Optional start date filter (YYYY-MM-DD format)
    - end_date: Optional end date filter (YYYY-MM-DD format)
    
    Returns monthly medical visit counts grouped by year-month (YYYY-MM format)
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    medical_records = list(db.medical_records.find())
    monthly_count = Counter()
    
    start_dt, end_dt, date_metadata = parse_date_range(start_date, end_date)
    
    valid_dates = 0
    invalid_dates = 0
    
    for record in medical_records:
        visit_date = record.get('visit_date', '')
        if visit_date:
            try:
                # Try parsing the date
                date_obj = datetime.strptime(str(visit_date), '%Y-%m-%d')
                valid_dates += 1
                
                # Apply date filters
                if start_dt and date_obj < start_dt:
                    continue
                if end_dt and date_obj > end_dt:
                    continue
                
                month_key = date_obj.strftime('%Y-%m')
                monthly_count[month_key] += 1
            except (ValueError, TypeError) as e:
                invalid_dates += 1
                # Log for debugging
                print(f"Invalid visit_date format: {visit_date}, error: {e}")
    
    # Sort by month
    sorted_months = sorted(monthly_count.items())
    
    metadata = {
        'total_records': len(medical_records),
        'valid_dates': valid_dates,
        'invalid_dates': invalid_dates,
        'filtered_count': sum(monthly_count.values()),
        **date_metadata
    }
    
    return {
        'labels': [item[0] for item in sorted_months],
        'data': [item[1] for item in sorted_months],
        'metadata': metadata
    }


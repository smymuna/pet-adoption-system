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
from bson import ObjectId

from backend.database.connection import get_database
from backend.species_breeds import SPECIES_BREEDS

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def charts_page(request: Request):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't reach database")
    
    # Get filter options
    species_list = sorted(set(a.get('species', '') for a in db.animals.find() if a.get('species')))
    status_list = sorted(set(a.get('status', '') for a in db.animals.find() if a.get('status')))
    gender_list = sorted(set(a.get('gender', '') for a in db.animals.find() if a.get('gender')))
    
    return templates.TemplateResponse("charts.html", {
        "request": request,
        "species_list": species_list,
        "status_list": status_list,
        "gender_list": gender_list,
        "species_breeds": SPECIES_BREEDS
    })


def build_animal_filter(species: Optional[str] = None, status: Optional[str] = None, 
                       gender: Optional[str] = None, breed: Optional[str] = None):
    """Build MongoDB filter dict from query params - only includes non-None values"""
    filter_dict = {}
    
    # Add filters only if they're provided
    if species:
        filter_dict['species'] = species
    if status:
        filter_dict['status'] = status
    if gender:
        filter_dict['gender'] = gender
    if breed:
        filter_dict['breed'] = breed
    
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


@router.get("/breed", response_model=Dict)
async def get_breed_distribution(
    species: Optional[str] = Query(None, description="Filter by species (required for breed distribution)"),
    status: Optional[str] = Query(None, description="Filter by animal status"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed (for consistency)")
):
    """Get breed distribution for a selected species with optional filters"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't reach database")
    
    if not species:
        return {
            'labels': [],
            'data': [],
            'message': 'Please select a species to view breed distribution'
        }
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
    animals = db.animals.find(filter_dict)
    breed_count = Counter(
        animal.get('breed', 'Unknown') 
        for animal in animals 
        if animal.get('breed') is not None
    )
    
    # Sort by count descending
    sorted_breeds = sorted(breed_count.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'labels': [item[0] for item in sorted_breeds],
        'data': [item[1] for item in sorted_breeds]
    }


@router.get("/species", response_model=Dict)
async def get_species_distribution(
    species: Optional[str] = Query(None, description="Filter by species (for consistency)"),
    status: Optional[str] = Query(None, description="Filter by animal status"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed")
):
    """Get animal species distribution with optional filters"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB connection error")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
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
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed")
):
    """Get animal status distribution (Available, Adopted, Medical)"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
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
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed")
):
    """Get age distribution grouped into ranges"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
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
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get monthly adoption numbers with optional filters
    
    Parameters:
    - species: Optional species filter
    - status: Optional status filter
    - gender: Optional gender filter
    - breed: Optional breed filter
    - start_date: Optional start date filter (YYYY-MM-DD format)
    - end_date: Optional end date filter (YYYY-MM-DD format)
    
    Returns monthly adoption counts grouped by year-month (YYYY-MM format)
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    # Build animal filter
    animal_filter = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
    # Get matching animal IDs
    matching_animals = set()
    if animal_filter:
        for animal in db.animals.find(animal_filter):
            matching_animals.add(str(animal['_id']))
    
    adoptions = list(db.adoptions.find())
    monthly_count = Counter()
    
    start_dt, end_dt, date_metadata = parse_date_range(start_date, end_date)
    
    valid_dates = 0
    invalid_dates = 0
    
    for adoption in adoptions:
        # Filter by animal if filters are provided
        if animal_filter:
            adoption_animal_id = adoption.get('animal_id')
            adoption_animal_id_str = str(adoption_animal_id) if adoption_animal_id else None
            
            if not adoption_animal_id_str or adoption_animal_id_str not in matching_animals:
                continue
        
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
    
    # If date range is provided, generate all months in the range
    if start_dt or end_dt:
        # Determine the range
        if start_dt and end_dt:
            # Both dates provided - use the range
            start_year = start_dt.year
            start_month = start_dt.month
            end_year = end_dt.year
            end_month = end_dt.month
        elif start_dt:
            # Only start date - go from start to current month
            start_year = start_dt.year
            start_month = start_dt.month
            now = datetime.now()
            end_year = now.year
            end_month = now.month
        else:  # end_dt only
            # Only end date - go from earliest adoption to end
            # Find earliest month with data, or use a reasonable default
            if monthly_count:
                earliest_month = min(monthly_count.keys())
                start_year, start_month = map(int, earliest_month.split('-'))
            else:
                # No data, use end date as start
                start_year = end_dt.year
                start_month = end_dt.month
            end_year = end_dt.year
            end_month = end_dt.month
        
        # Generate all months from start to end
        all_months = []
        year = start_year
        month = start_month
        
        while (year, month) <= (end_year, end_month):
            month_key = f"{year:04d}-{month:02d}"
            all_months.append(month_key)
            # Move to next month
            month += 1
            if month > 12:
                month = 1
                year += 1
        
        # Fill in data for all months (0 if no adoptions)
        labels = all_months
        data = [monthly_count.get(month, 0) for month in all_months]
    else:
        # No date range - just return months with data
        sorted_months = sorted(monthly_count.items())
        labels = [item[0] for item in sorted_months]
        data = [item[1] for item in sorted_months]
    
    metadata = {
        'total_adoptions': len(adoptions),
        'valid_dates': valid_dates,
        'invalid_dates': invalid_dates,
        'filtered_count': sum(monthly_count.values()),
        **date_metadata
    }
    
    return {
        'labels': labels,
        'data': data,
        'metadata': metadata
    }


@router.get("/adoption-rate", response_model=Dict)
async def get_adoption_rate_by_species(
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed")
):
    """Get adoption rate (adopted vs available) by species with optional filters"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Can't connect to database")
    
    # Apply filters to animals
    filter_dict = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
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
    gender: Optional[str] = Query(None, description="Filter by gender (for consistency)"),
    breed: Optional[str] = Query(None, description="Filter by breed")
):
    """Get gender distribution"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB connection error")
    
    filter_dict = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
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
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get medical visits over time with optional filters
    
    Parameters:
    - species: Optional species filter
    - status: Optional status filter
    - gender: Optional gender filter
    - breed: Optional breed filter
    - start_date: Optional start date filter (YYYY-MM-DD format)
    - end_date: Optional end date filter (YYYY-MM-DD format)
    
    Returns monthly medical visit counts grouped by year-month (YYYY-MM format)
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    # Build animal filter
    animal_filter = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
    # Get matching animal IDs
    matching_animals = set()
    if animal_filter:
        for animal in db.animals.find(animal_filter):
            matching_animals.add(str(animal['_id']))
    
    medical_records = list(db.medical_records.find())
    monthly_count = Counter()
    
    start_dt, end_dt, date_metadata = parse_date_range(start_date, end_date)
    
    valid_dates = 0
    invalid_dates = 0
    
    for record in medical_records:
        # Filter by animal if filters are provided
        if animal_filter and str(record.get('animal_id')) not in matching_animals:
            continue
        
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
    
    # If date range is provided, generate all months in the range
    if start_dt or end_dt:
        # Determine the range
        if start_dt and end_dt:
            # Both dates provided - use the range
            start_year = start_dt.year
            start_month = start_dt.month
            end_year = end_dt.year
            end_month = end_dt.month
        elif start_dt:
            # Only start date - go from start to current month
            start_year = start_dt.year
            start_month = start_dt.month
            now = datetime.now()
            end_year = now.year
            end_month = now.month
        else:  # end_dt only
            # Only end date - go from earliest visit to end
            # Find earliest month with data, or use a reasonable default
            if monthly_count:
                earliest_month = min(monthly_count.keys())
                start_year, start_month = map(int, earliest_month.split('-'))
            else:
                # No data, use end date as start
                start_year = end_dt.year
                start_month = end_dt.month
            end_year = end_dt.year
            end_month = end_dt.month
        
        # Generate all months from start to end
        all_months = []
        year = start_year
        month = start_month
        
        while (year, month) <= (end_year, end_month):
            month_key = f"{year:04d}-{month:02d}"
            all_months.append(month_key)
            # Move to next month
            month += 1
            if month > 12:
                month = 1
                year += 1
        
        # Fill in data for all months (0 if no visits)
        labels = all_months
        data = [monthly_count.get(month, 0) for month in all_months]
    else:
        # No date range - just return months with data
        sorted_months = sorted(monthly_count.items())
        labels = [item[0] for item in sorted_months]
        data = [item[1] for item in sorted_months]
    
    metadata = {
        'total_records': len(medical_records),
        'valid_dates': valid_dates,
        'invalid_dates': invalid_dates,
        'filtered_count': sum(monthly_count.values()),
        **date_metadata
    }
    
    return {
        'labels': labels,
        'data': data,
        'metadata': metadata
    }


@router.get("/medical-visits-by-species", response_model=Dict)
async def get_medical_visits_by_species(
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get medical visit frequency by species with optional filters
    
    Parameters:
    - species: Optional species filter
    - status: Optional status filter
    - gender: Optional gender filter
    - breed: Optional breed filter
    - start_date: Optional start date filter (YYYY-MM-DD format)
    - end_date: Optional end date filter (YYYY-MM-DD format)
    
    Returns medical visit counts grouped by species
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Connection failed")
    
    # Build animal filter (include species if provided, but we'll still group by all species)
    animal_filter = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
    # Get matching animal IDs
    matching_animals = set()
    if animal_filter:
        for animal in db.animals.find(animal_filter):
            matching_animals.add(str(animal['_id']))
    
    medical_records = list(db.medical_records.find())
    species_count = Counter()
    
    start_dt, end_dt, date_metadata = parse_date_range(start_date, end_date)
    
    for record in medical_records:
        # Filter by animal if filters are provided
        if animal_filter and str(record.get('animal_id')) not in matching_animals:
            continue
        
        visit_date = record.get('visit_date', '')
        animal_id = record.get('animal_id')
        
        # Apply date filter if provided
        if visit_date:
            try:
                date_obj = datetime.strptime(str(visit_date), '%Y-%m-%d')
                if start_dt and date_obj < start_dt:
                    continue
                if end_dt and date_obj > end_dt:
                    continue
            except (ValueError, TypeError):
                continue
        
        # Get animal species
        if animal_id:
            try:
                animal = db.animals.find_one({'_id': ObjectId(animal_id)})
                if animal:
                    species_name = animal.get('species', 'Unknown')
                    species_count[species_name] += 1
            except Exception:
                continue
    
    # Sort by count descending
    sorted_species = sorted(species_count.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'labels': [item[0] for item in sorted_species],
        'data': [item[1] for item in sorted_species]
    }


@router.get("/medical-visits-by-breed", response_model=Dict)
async def get_medical_visits_by_breed(
    species: Optional[str] = Query(None, description="Filter by species (required for breed distribution)"),
    status: Optional[str] = Query(None, description="Filter by status"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    breed: Optional[str] = Query(None, description="Filter by breed (for consistency)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get medical visit frequency by breed for a selected species with optional filters
    
    Parameters:
    - species: Required species filter
    - status: Optional status filter
    - gender: Optional gender filter
    - breed: Optional breed filter (for consistency)
    - start_date: Optional start date filter (YYYY-MM-DD format)
    - end_date: Optional end date filter (YYYY-MM-DD format)
    
    Returns medical visit counts grouped by breed for the selected species
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="DB error")
    
    if not species:
        return {
            'labels': [],
            'data': [],
            'message': 'Please select a species to view medical visits by breed'
        }
    
    # Build animal filter
    animal_filter = build_animal_filter(species=species, status=status, gender=gender, breed=breed)
    
    # Get matching animal IDs
    matching_animals = set()
    if animal_filter:
        for animal in db.animals.find(animal_filter):
            matching_animals.add(str(animal['_id']))
    
    medical_records = list(db.medical_records.find())
    breed_count = Counter()
    
    start_dt, end_dt, date_metadata = parse_date_range(start_date, end_date)
    
    for record in medical_records:
        # Filter by animal if filters are provided
        if animal_filter and str(record.get('animal_id')) not in matching_animals:
            continue
        
        visit_date = record.get('visit_date', '')
        animal_id = record.get('animal_id')
        
        # Apply date filter if provided
        if visit_date:
            try:
                date_obj = datetime.strptime(str(visit_date), '%Y-%m-%d')
                if start_dt and date_obj < start_dt:
                    continue
                if end_dt and date_obj > end_dt:
                    continue
            except (ValueError, TypeError):
                continue
        
        # Get animal breed for selected species
        if animal_id:
            try:
                animal = db.animals.find_one({'_id': ObjectId(animal_id)})
                if animal and animal.get('species') == species:
                    breed_name = animal.get('breed', 'Unknown')
                    breed_count[breed_name] += 1
            except Exception:
                continue
    
    # Sort by count descending
    sorted_breeds = sorted(breed_count.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'labels': [item[0] for item in sorted_breeds],
        'data': [item[1] for item in sorted_breeds]
    }

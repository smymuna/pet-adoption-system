# Pet Adoption System - Presentation Guide

## 📋 Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Where Queries Are Located](#where-queries-are-located)
3. [Complex Queries Explained](#complex-queries-explained)
4. [CRUD Operations Demo](#crud-operations-demo)
5. [Presentation Flow](#presentation-flow)
6. [Code Snippets to Show](#code-snippets-to-show)

---

## 🏗️ System Architecture Overview

### Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: MongoDB (Local)
- **Frontend**: HTML/CSS/JavaScript + Bootstrap 5
- **Visualization**: Chart.js

### Project Structure
```
pet-adoption-system/
├── backend/
│   ├── api/routes/          # All API endpoints & queries
│   │   ├── animals.py       # Animal CRUD operations
│   │   ├── adoptions.py     # Adoption CRUD + joins
│   │   ├── charts.py        # Complex aggregation queries
│   │   ├── search.py        # Search queries with joins
│   │   └── ...
│   ├── database/
│   │   └── connection.py   # MongoDB connection
│   └── models.py           # Data validation models
├── frontend/
│   └── templates/          # HTML pages
└── main.py                # Application entry point
```

---

## 📍 Where Queries Are Located

### 1. **CRUD Operations**
**Location**: `backend/api/routes/[entity].py`

- `animals.py` - Lines 36-128
- `adopters.py` - Lines 36-128
- `adoptions.py` - Lines 40-143
- `medical.py` - Lines 40-109
- `volunteers.py` - Lines 40-97

### 2. **Complex Queries & Aggregations**
**Location**: `backend/api/routes/charts.py`

- **Monthly Adoptions** - Lines 183-244
- **Adoption Rate by Species** - Lines 247-291
- **Medical Visits Over Time** - Lines 320-381
- **Filtered Distributions** - Lines 87-317

### 3. **Search Queries with Joins**
**Location**: `backend/api/routes/search.py`

- **Search by Adopter** - Lines 29-47 (joins adoptions + animals)
- **Search Medical Records** - Lines 61-73

### 4. **Database Connection**
**Location**: `backend/database/connection.py`

- Connection management - Lines 15-30
- Document serialization - Lines 42-47

---

## 🔍 Complex Queries Explained

### Query 1: Monthly Adoptions with Date Filtering
**File**: `backend/api/routes/charts.py` (Lines 183-244)

**What it does**: Groups adoptions by month and applies date range filters

```python
@router.get("/adoptions", response_model=Dict)
async def get_monthly_adoptions(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    db = get_database()
    adoptions = list(db.adoptions.find())  # Get all adoptions
    monthly_count = Counter()
    
    # Parse and validate date filters
    start_dt, end_dt, date_metadata = parse_date_range(start_date, end_date)
    
    # Process each adoption
    for adoption in adoptions:
        adoption_date = adoption.get('adoption_date', '')
        if adoption_date:
            date_obj = datetime.strptime(str(adoption_date), '%Y-%m-%d')
            
            # Apply date filters
            if start_dt and date_obj < start_dt:
                continue
            if end_dt and date_obj > end_dt:
                continue
            
            # Group by year-month
            month_key = date_obj.strftime('%Y-%m')
            monthly_count[month_key] += 1
    
    # Return sorted results
    sorted_months = sorted(monthly_count.items())
    return {
        'labels': [item[0] for item in sorted_months],
        'data': [item[1] for item in sorted_months],
        'metadata': {...}
    }
```

**Complexity Points**:
- ✅ Date parsing and validation
- ✅ Date range filtering
- ✅ Data aggregation (grouping by month)
- ✅ Error handling for invalid dates
- ✅ Metadata tracking

---

### Query 2: Adoption Rate by Species (Multi-Collection Join)
**File**: `backend/api/routes/charts.py` (Lines 247-291)

**What it does**: Calculates adoption rates by joining animals and adoptions collections

```python
@router.get("/adoption-rate", response_model=Dict)
async def get_adoption_rate_by_species(
    species: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    gender: Optional[str] = Query(None)
):
    db = get_database()
    
    # Apply filters to animals
    filter_dict = build_animal_filter(species=species, status=status, gender=gender)
    animals = db.animals.find(filter_dict)
    adoptions = db.adoptions.find()
    
    # Get all adopted animal IDs (set for O(1) lookup)
    adopted_ids = {str(ad['animal_id']) for ad in adoptions}
    
    # Count by species
    species_stats = defaultdict(lambda: {'total': 0, 'adopted': 0})
    
    for animal in animals:
        species_name = animal.get('species', 'Unknown')
        animal_id = str(animal['_id'])
        species_stats[species_name]['total'] += 1
        if animal_id in adopted_ids:  # Check if adopted
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
```

**Complexity Points**:
- ✅ Multi-collection join (animals + adoptions)
- ✅ Set-based lookup for performance
- ✅ Dynamic filtering (species, status, gender)
- ✅ Aggregation with calculations
- ✅ Data transformation for visualization

---

### Query 3: Search by Adopter (Join Query)
**File**: `backend/api/routes/search.py` (Lines 29-47)

**What it does**: Finds all animals adopted by a specific adopter (joins 3 collections)

```python
@router.get("/adopter/{adopter_id}", response_model=List[Dict])
async def search_by_adopter(adopter_id: str):
    db = get_database()
    
    # Find all adoptions for this adopter
    adoptions = db.adoptions.find({'adopter_id': adopter_id})
    animals_list = []
    
    # Join with animals collection
    for adoption in adoptions:
        animal = db.animals.find_one({'_id': ObjectId(adoption['animal_id'])})
        if animal:
            animal_doc = serialize_doc(animal)
            animal_doc['adoption_date'] = adoption.get('adoption_date', '')
            animals_list.append(animal_doc)
    
    return animals_list
```

**Complexity Points**:
- ✅ Collection join (adoptions → animals)
- ✅ Data enrichment (adding adoption_date to animal data)
- ✅ Error handling

---

### Query 4: Adoption Page with Multiple Joins
**File**: `backend/api/routes/adoptions.py` (Lines 20-37)

**What it does**: Displays adoptions with joined animal and adopter information

```python
@router.get("/page", response_class=HTMLResponse)
async def adoptions_page(request: Request):
    db = get_database()
    
    adoptions_list = []
    for adoption in db.adoptions.find():
        adoption_doc = serialize_doc(adoption)
        
        # Join with animals collection
        animal = db.animals.find_one({'_id': ObjectId(adoption['animal_id'])})
        # Join with adopters collection
        adopter = db.adopters.find_one({'_id': ObjectId(adoption['adopter_id'])})
        
        # Enrich adoption data
        adoption_doc['animal_name'] = animal['name'] if animal else 'Unknown'
        adoption_doc['adopter_name'] = adopter['name'] if adopter else 'Unknown'
        adoptions_list.append(adoption_doc)
    
    return templates.TemplateResponse("adoptions.html", {
        "request": request, 
        "adoptions": adoptions_list
    })
```

**Complexity Points**:
- ✅ Multiple collection joins (adoptions → animals + adopters)
- ✅ Data enrichment
- ✅ Null handling

---

## 🎯 CRUD Operations Demo

### CREATE Operation
**File**: `backend/api/routes/animals.py` (Lines 58-68)

```python
@router.post("", response_model=AnimalResponse)
async def create_animal(animal: AnimalCreate):
    db = get_database()
    
    # Convert Pydantic model to dict
    animal_dict = animal.dict()
    
    # Insert into MongoDB
    result = db.animals.insert_one(animal_dict)
    
    # Fetch and return created document
    created_animal = db.animals.find_one({'_id': result.inserted_id})
    return serialize_doc(created_animal)
```

**Demo Steps**:
1. Go to `/animals` page
2. Click "Add New Animal"
3. Fill in form (name, species, breed, age, gender, status)
4. Click "Create Animal"
5. Show the new animal appears in the list

---

### READ Operation
**File**: `backend/api/routes/animals.py` (Lines 36-49)

```python
@router.get("", response_model=List[AnimalResponse])
async def get_animals():
    db = get_database()
    
    # Query all animals
    animals_list = []
    for a in db.animals.find():
        # Filter incomplete records
        if all(key in a for key in ['name', 'species', 'age', 'gender', 'status']):
            animals_list.append(serialize_doc(a))
    
    return animals_list
```

**Demo Steps**:
1. Go to `/animals` page
2. Show list of all animals
3. Explain the filtering logic (removes incomplete records)

---

### UPDATE Operation
**File**: `backend/api/routes/animals.py` (Lines 89-110)

```python
@router.put("/{animal_id}", response_model=AnimalResponse)
async def update_animal(animal_id: str, animal: AnimalUpdate):
    db = get_database()
    
    # Convert ObjectId
    animal_id_obj = ObjectId(animal_id)
    
    # Prepare update data (only non-null fields)
    update_data = {k: v for k, v in animal.dict().items() if v is not None}
    
    # Update document
    result = db.animals.update_one(
        {'_id': animal_id_obj}, 
        {'$set': update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Fetch and return updated document
    updated_animal = db.animals.find_one({'_id': animal_id_obj})
    return serialize_doc(updated_animal)
```

**Demo Steps**:
1. Go to `/animals` page
2. Click "Edit" on an animal
3. Change some fields (e.g., status from "Available" to "Medical")
4. Click "Update Animal"
5. Show the change is reflected immediately

---

### DELETE Operation
**File**: `backend/api/routes/animals.py` (Lines 113-128)

```python
@router.delete("/{animal_id}", response_model=SuccessResponse)
async def delete_animal(animal_id: str):
    db = get_database()
    
    # Convert ObjectId
    animal_id_obj = ObjectId(animal_id)
    
    # Delete document
    result = db.animals.delete_one({'_id': animal_id_obj})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    return SuccessResponse(success=True, message="Animal deleted successfully")
```

**Demo Steps**:
1. Go to `/animals` page
2. Click "Delete" on an animal
3. Confirm deletion
4. Show animal is removed from list

---

### Complex CREATE: Adoption with Status Update
**File**: `backend/api/routes/adoptions.py` (Lines 51-76)

```python
@router.post("", response_model=AdoptionResponse)
async def create_adoption(adoption: AdoptionCreate):
    db = get_database()
    
    # Validate animal exists
    animal = db.animals.find_one({'_id': ObjectId(adoption.animal_id)})
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Validate adopter exists
    adopter = db.adopters.find_one({'_id': ObjectId(adoption.adopter_id)})
    if not adopter:
        raise HTTPException(status_code=404, detail="Adopter not found")
    
    # Prepare adoption data
    adoption_dict = adoption.dict()
    if not adoption_dict.get('adoption_date'):
        adoption_dict['adoption_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Update animal status to "Adopted"
    db.animals.update_one(
        {'_id': ObjectId(adoption.animal_id)}, 
        {'$set': {'status': 'Adopted'}}
    )
    
    # Create adoption record
    result = db.adoptions.insert_one(adoption_dict)
    adoption_dict['_id'] = str(result.inserted_id)
    return adoption_dict
```

**Complexity Points**:
- ✅ Multi-collection validation
- ✅ Automatic status update
- ✅ Default date assignment
- ✅ Transaction-like behavior

**Demo Steps**:
1. Go to `/adoptions` page
2. Click "Add New Adoption"
3. Select an animal (show it's "Available")
4. Select an adopter
5. Create adoption
6. Show:
   - Adoption appears in list
   - Animal status changed to "Adopted" (go back to animals page)

---

## 🎤 Presentation Flow

### 1. Introduction (2 minutes)
- **What**: Pet Adoption & Animal Shelter Management System
- **Tech Stack**: FastAPI, MongoDB, Bootstrap 5, Chart.js
- **Purpose**: Manage animals, adoptions, medical records, volunteers

### 2. System Architecture (3 minutes)
- Show project structure
- Explain layered architecture (Routes → Database → MongoDB)
- Show `backend/database/connection.py` - connection management

### 3. CRUD Operations Demo (5 minutes)

**Animals CRUD**:
1. **CREATE**: Add a new animal
   - Show form validation
   - Show code: `animals.py` lines 58-68
   - Show MongoDB insert operation

2. **READ**: View all animals
   - Show filtering logic
   - Show code: `animals.py` lines 36-49
   - Explain data validation

3. **UPDATE**: Edit an animal
   - Change status from "Available" to "Medical"
   - Show code: `animals.py` lines 89-110
   - Show `$set` update operation

4. **DELETE**: Remove an animal
   - Show code: `animals.py` lines 113-128
   - Show MongoDB delete operation

### 4. Complex Queries Demo (8 minutes)

**Query 1: Monthly Adoptions**
1. Go to `/charts` page
2. Show "Monthly Adoptions" chart
3. Apply date filters (start_date, end_date)
4. Show code: `charts.py` lines 183-244
5. Explain:
   - Date parsing
   - Date range filtering
   - Aggregation by month
   - Error handling

**Query 2: Adoption Rate by Species**
1. Show "Adoption Rate by Species" chart
2. Apply filters (species, status, gender)
3. Show code: `charts.py` lines 247-291
4. Explain:
   - Multi-collection join
   - Set-based lookup
   - Aggregation calculation

**Query 3: Search by Adopter**
1. Go to `/search/adopter` page
2. Select an adopter
3. Show all their adopted animals
4. Show code: `search.py` lines 29-47
5. Explain:
   - Collection join
   - Data enrichment

### 5. Advanced Features (3 minutes)

**Complex CREATE: Adoption with Status Update**
1. Go to `/adoptions` page
2. Create a new adoption
3. Show code: `adoptions.py` lines 51-76
4. Explain:
   - Multi-collection validation
   - Automatic status update
   - Transaction-like behavior

**Adoption Page with Joins**
1. Show adoptions page with animal and adopter names
2. Show code: `adoptions.py` lines 20-37
3. Explain multiple collection joins

### 6. Data Visualization (2 minutes)
- Show all 7 charts
- Explain filtering system
- Show how filters apply across charts

### 7. Code Highlights (2 minutes)
- Show key code files
- Explain query patterns
- Show error handling

### 8. Q&A (remaining time)

---

## 💻 Code Snippets to Show

### Snippet 1: Database Connection
**File**: `backend/database/connection.py`

```python
def get_database() -> Optional[Database]:
    """Get MongoDB database instance (Singleton pattern)"""
    global _client, _database
    
    if _database is not None:
        return _database  # Reuse existing connection
    
    try:
        _client = MongoClient(MONGO_URI)
        _database = _client[DB_NAME]
        _database.command('ping')  # Test connection
        return _database
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None
```

**Key Points**:
- Singleton pattern for connection reuse
- Connection pooling handled by PyMongo
- Error handling

---

### Snippet 2: Complex Aggregation Query
**File**: `backend/api/routes/charts.py` (Lines 247-291)

```python
# Get all adopted animal IDs (set for O(1) lookup)
adopted_ids = {str(ad['animal_id']) for ad in adoptions}

# Count by species with adoption status
species_stats = defaultdict(lambda: {'total': 0, 'adopted': 0})

for animal in animals:
    species_name = animal.get('species', 'Unknown')
    animal_id = str(animal['_id'])
    species_stats[species_name]['total'] += 1
    if animal_id in adopted_ids:  # O(1) lookup
        species_stats[species_name]['adopted'] += 1
```

**Key Points**:
- Set-based lookup for performance
- Aggregation with calculations
- Efficient data structure

---

### Snippet 3: Multi-Collection Join
**File**: `backend/api/routes/adoptions.py` (Lines 20-37)

```python
for adoption in db.adoptions.find():
    adoption_doc = serialize_doc(adoption)
    
    # Join with animals collection
    animal = db.animals.find_one({'_id': ObjectId(adoption['animal_id'])})
    # Join with adopters collection
    adopter = db.adopters.find_one({'_id': ObjectId(adoption['adopter_id'])})
    
    # Enrich adoption data
    adoption_doc['animal_name'] = animal['name'] if animal else 'Unknown'
    adoption_doc['adopter_name'] = adopter['name'] if adopter else 'Unknown'
```

**Key Points**:
- Multiple collection joins
- Data enrichment
- Null handling

---

### Snippet 4: Transaction-like Operation
**File**: `backend/api/routes/adoptions.py` (Lines 51-76)

```python
# Validate both collections
animal = db.animals.find_one({'_id': ObjectId(adoption.animal_id)})
adopter = db.adopters.find_one({'_id': ObjectId(adoption.adopter_id)})

# Update animal status
db.animals.update_one(
    {'_id': ObjectId(adoption.animal_id)}, 
    {'$set': {'status': 'Adopted'}}
)

# Create adoption record
result = db.adoptions.insert_one(adoption_dict)
```

**Key Points**:
- Multi-collection validation
- Atomic-like operations
- Data consistency

---

## 🎯 Quick Reference: File Locations

| Feature | File | Lines |
|---------|------|-------|
| **Database Connection** | `backend/database/connection.py` | 15-30 |
| **Animal CRUD** | `backend/api/routes/animals.py` | 36-128 |
| **Adoption CRUD** | `backend/api/routes/adoptions.py` | 40-143 |
| **Monthly Adoptions** | `backend/api/routes/charts.py` | 183-244 |
| **Adoption Rate** | `backend/api/routes/charts.py` | 247-291 |
| **Search by Adopter** | `backend/api/routes/search.py` | 29-47 |
| **Medical Records** | `backend/api/routes/medical.py` | 40-109 |

---

## 📝 Presentation Tips

1. **Start with Live Demo**: Show the working website first
2. **Show Code After Demo**: Explain what you just showed
3. **Use Browser DevTools**: Show API calls in Network tab
4. **Highlight Complexity**: Point out joins, aggregations, filtering
5. **Show Error Handling**: Demonstrate validation and error messages
6. **Explain Performance**: Mention set-based lookups, connection pooling
7. **Show Data Flow**: Request → Route → Database → Response

---

## 🚀 Quick Start Commands

```bash
# Start the application
python main.py

# Access the website
http://localhost:5001

# Test MongoDB connection
python utils/test_mongodb_connection.py

# View API documentation
http://localhost:5001/docs
```

---

## 📊 Database Collections

1. **animals** - Animal records
2. **adopters** - Adopter information
3. **adoptions** - Adoption records (joins animals + adopters)
4. **medical_records** - Medical history (linked to animals)
5. **volunteers** - Volunteer information

---

Good luck with your presentation! 🎉


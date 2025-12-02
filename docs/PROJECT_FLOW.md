# Project Flow - Pet Adoption System

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│  (HTML Pages: Dashboard, Animals, Adopters, etc.)           │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI APPLICATION (main.py)                  │
│  - Routes requests to appropriate handlers                  │
│  - Handles static files and templates                      │
└──────────────────────┬───────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ↓              ↓              ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Page Routes  │ │  API Routes  │ │ Chart Routes │
│ (HTML)       │ │  (JSON)      │ │ (JSON)       │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│         DATABASE CONNECTION LAYER                           │
│  (backend/database/connection.py)                          │
│  - Manages MongoDB connection                              │
│  - Handles serialization                                   │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              MONGODB DATABASE                               │
│  Collections:                                               │
│  - animals                                                  │
│  - adopters                                                 │
│  - adoptions                                                │
│  - medical_records                                          │
│  - volunteers                                               │
│  - volunteer_activities                                     │
└─────────────────────────────────────────────────────────────┘
```

## Request Processing Flow

### 1. Page Request Flow (HTML Rendering)

```
User clicks link → GET /animals
    ↓
FastAPI router matches route
    ↓
animals_page() function called
    ↓
get_database() → MongoDB connection
    ↓
Query: db.animals.find()
    ↓
Serialize results (ObjectId → string)
    ↓
Enrich data (add volunteer names, etc.)
    ↓
Jinja2 template rendering
    ↓
HTML response with embedded data
    ↓
Browser displays page
```

### 2. API Request Flow (JSON)

```
JavaScript fetch() → GET /api/animals
    ↓
FastAPI router matches route
    ↓
get_animals() function called
    ↓
get_database() → MongoDB connection
    ↓
Query: db.animals.find()
    ↓
Filter incomplete records
    ↓
Serialize all results
    ↓
Return JSON array
    ↓
JavaScript processes data
    ↓
Update DOM dynamically
```

### 3. Create Operation Flow

```
User fills form → Submit button
    ↓
JavaScript collects form data
    ↓
POST /api/animals with JSON body
    ↓
Pydantic model validates input (AnimalCreate)
    ↓
get_database() → MongoDB connection
    ↓
Convert to dict: animal.dict()
    ↓
db.animals.insert_one(animal_dict)
    ↓
Get inserted document
    ↓
Serialize (ObjectId → string)
    ↓
Return JSON response
    ↓
JavaScript updates UI
    ↓
Page refreshes or table updates
```

### 4. Update Operation Flow

```
User clicks Edit → Form pre-filled
    ↓
User modifies data → Submit
    ↓
PUT /api/animals/{id} with JSON body
    ↓
Pydantic model validates (AnimalUpdate)
    ↓
Validate ObjectId format
    ↓
Filter out None values from update
    ↓
db.animals.update_one({'_id': id}, {'$set': update_data})
    ↓
Fetch updated document
    ↓
Serialize and return
    ↓
UI updates with new data
```

### 5. Delete Operation Flow

```
User clicks Delete → Confirmation
    ↓
DELETE /api/animals/{id}
    ↓
Validate ObjectId format
    ↓
db.animals.delete_one({'_id': id})
    ↓
Check deleted_count
    ↓
Return success response
    ↓
JavaScript removes row from table
```

## Data Flow Patterns

### Animal with Volunteers Flow

```
GET /animals (page)
    ↓
Query animals from MongoDB
    ↓
For each animal:
    ↓
    Check if assigned_volunteers exists
    ↓
    For each volunteer_id:
        ↓
        Query volunteers collection
        ↓
        Get volunteer name
        ↓
    Build volunteer_info array
    ↓
Add to animal document
    ↓
Render template with enriched data
```

### Adoption Creation Flow

```
POST /api/adoptions
    ↓
Validate animal_id and adopter_id
    ↓
Check animal exists
    ↓
Check adopter exists
    ↓
Create adoption record
    ↓
**Automatically update animal status**
    ↓
db.animals.update_one({'_id': animal_id}, {'$set': {'status': 'Adopted'}})
    ↓
Return adoption response
```

### Chart Data Flow

```
GET /api/charts/species?species=Dog&status=Available
    ↓
Parse query parameters
    ↓
build_animal_filter() creates MongoDB filter
    ↓
Query: db.animals.find({'species': 'Dog', 'status': 'Available'})
    ↓
Count occurrences
    ↓
Group by species
    ↓
Return: {'labels': [...], 'data': [...]}
    ↓
Frontend Chart.js renders chart
```

### Volunteer Activity Statistics Flow

```
GET /api/volunteer-activities/stats/summary
    ↓
Query all activities
    ↓
Calculate total_hours (sum duration_minutes / 60)
    ↓
Group by activity_type
    ↓
Count activities per volunteer
    ↓
Sort by hours (top volunteers)
    ↓
Return comprehensive stats object
```

## Cross-Collection Queries

### Finding Animals by Adopter

```
GET /api/search/adopter/{adopter_id}
    ↓
Query adoptions: {'adopter_id': ObjectId(adopter_id)}
    ↓
Extract animal_ids from adoptions
    ↓
Query animals: {'_id': {'$in': [animal_ids]}}
    ↓
Return list of animals
```

### Medical Records with Animal Names

```
GET /medical (page)
    ↓
Query medical_records
    ↓
For each record:
    ↓
    Extract animal_id
    ↓
    Query animals: {'_id': ObjectId(animal_id)}
    ↓
    Get animal name
    ↓
    Add to record document
    ↓
Render with animal names
```

### Volunteer Suggestions

```
GET /api/animals/{id}/suggested-volunteers
    ↓
Get animal (get species)
    ↓
get_skills_for_species(animal.species)
    ↓
Query volunteers with matching skills
    ↓
For each volunteer:
    ↓
    Check if already assigned
    ↓
    Calculate matching score
    ↓
Sort by relevance
    ↓
Return suggested list
```

## Filter Application Flow

### Chart Filtering

```
User selects filters (species, status, gender, breed, dates)
    ↓
JavaScript builds query string
    ↓
All chart endpoints called with same filters
    ↓
Each endpoint:
    ↓
    build_animal_filter() creates MongoDB filter
    ↓
    parse_date_range() handles date filters
    ↓
    Apply filters to queries
    ↓
    Return filtered data
    ↓
All charts update simultaneously
```

### Animal Page Filtering

```
User selects species from dropdown
    ↓
JavaScript filters table rows client-side
    ↓
OR: Navigate with query parameter ?status=Available
    ↓
Backend reads query parameter
    ↓
Build filter: {'status': 'Available'}
    ↓
Query: db.animals.find(filter)
    ↓
Return filtered results
```

## Real-Time Updates

### Dashboard Statistics

```
GET /dashboard
    ↓
Query all collections:
    - Count animals
    - Count adopters
    - Count adoptions
    - Count volunteers
    ↓
Calculate volunteer hours:
    - Query all activities
    - Sum duration_minutes
    - Convert to hours
    ↓
Count animals needing volunteers:
    - Query available animals
    - Check assigned_volunteers array
    - Count empty arrays
    ↓
Return stats object
    ↓
Template renders cards with numbers
```

## Error Flow

```
Request → Route Handler
    ↓
get_database()
    ↓
If db is None:
    ↓
    Raise HTTPException(500, "DB error")
    ↓
Else:
    ↓
    Try operation
    ↓
    If error:
        ↓
        Catch exception
        ↓
        Raise HTTPException(400/404, message)
    ↓
FastAPI error handler
    ↓
JSON error response
    ↓
Frontend displays error message
```

## State Synchronization

- **No client-side state persistence** (stateless API)
- **Database is source of truth**
- **Each request queries fresh data**
- **Filters via URL parameters** (shareable links)
- **No caching** (always current data)


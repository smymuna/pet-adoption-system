# Pet Adoption System - Workflow Documentation

## System Overview

The Pet Adoption & Animal Shelter Management System (PASMS) is a full-stack web application that manages animal shelter operations including animal records, adoptions, medical records, volunteers, and comprehensive analytics.

## Application Architecture

### Technology Stack
- **Backend**: FastAPI (Python)
- **Database**: MongoDB (NoSQL)
- **Frontend**: HTML/CSS/JavaScript with Bootstrap 5
- **Templates**: Jinja2
- **Charts**: Chart.js

### Request Flow

```
User Browser
    ↓
FastAPI Application (main.py)
    ↓
Router (backend/api/routes/)
    ↓
Database Connection (backend/database/connection.py)
    ↓
MongoDB Database
    ↓
Response (JSON or HTML Template)
    ↓
User Browser
```

## User Workflows

### 1. Animal Management Workflow

**Adding a New Animal:**
1. Navigate to `/animals` page
2. Click "Add Animal" button
3. Fill in form: name, species, breed, age, gender, status, intake date, behavioral notes
4. Submit → POST `/api/animals`
5. Animal saved to MongoDB `animals` collection
6. Page refreshes showing new animal

**Updating Animal Status:**
1. Find animal in animals list
2. Click "Edit" button
3. Modify fields (e.g., change status from "Available" to "Adopted")
4. Submit → PUT `/api/animals/{id}`
5. Database updated, page refreshes

**Assigning Volunteers:**
1. Click "Assign Volunteer" on animal row
2. System suggests volunteers based on animal species and volunteer skills
3. Select volunteer → POST `/api/animals/{id}/assign-volunteer`
4. Volunteer added to animal's `assigned_volunteers` array
5. Badge appears in animals table

### 2. Adoption Workflow

**Creating an Adoption:**
1. Navigate to `/adoptions` page
2. Click "Add Adoption"
3. Select animal (must be "Available")
4. Select adopter (or create new one)
5. Set adoption date (defaults to today)
6. Submit → POST `/api/adoptions`
7. **Automatic Actions:**
   - Adoption record created in `adoptions` collection
   - Animal status automatically changed to "Adopted"
   - Animal removed from available list

**Viewing Adoption History:**
- All adoptions listed on `/adoptions` page
- Can search adoptions by adopter via `/search/adopter`

### 3. Medical Records Workflow

**Adding Medical Record:**
1. Navigate to `/medical` page
2. Click "Add Medical Record"
3. Select animal
4. Enter vet name, visit date, diagnosis, treatment, notes
5. Submit → POST `/api/medical`
6. Record saved to `medical_records` collection

**Viewing Medical History:**
- Search by animal via `/search/medical`
- Records sorted by visit date (newest first)
- All records displayed with animal name

### 4. Volunteer Management Workflow

**Registering Volunteer:**
1. Navigate to `/volunteers` page
2. Click "Add Volunteer"
3. Enter name, contact info
4. Select skills (multi-select from standardized list)
5. Set availability
6. Submit → POST `/api/volunteers`
7. Volunteer added to `volunteers` collection

**Logging Volunteer Activity:**
1. Navigate to `/volunteer-activities` page
2. Click "Add Activity"
3. Select volunteer and animal
4. Choose activity type (Walking, Feeding, Grooming, etc.)
5. Enter date and duration in minutes
6. Add optional notes
7. Submit → POST `/api/volunteer-activities`
8. Activity logged, hours tracked for statistics

**Skill-Based Matching:**
- System automatically suggests volunteers when assigning to animals
- Matches based on volunteer skills and animal species
- Example: Dog volunteers suggested for dog animals

### 5. Analytics & Reporting Workflow

**Viewing Charts:**
1. Navigate to `/charts` page
2. Charts organized into sections:
   - **Animal Demographics**: Species, Breed, Status, Age, Gender
   - **Adoption Analytics**: Monthly adoptions, Adoption rate by species
   - **Medical Analytics**: Medical visits over time, by species, by breed

**Applying Filters:**
1. Use filter dropdowns at top of charts page
2. Select: Species, Status, Gender, Breed
3. Set date range (for time-based charts)
4. All charts update automatically based on filters
5. Filters persist across all charts

**Dashboard Overview:**
- Navigate to `/dashboard` (home page)
- View key metrics:
  - Total animals, adopters, adoptions
  - Available vs Adopted animals
  - Volunteer statistics (hours, activities)
  - Animals needing volunteers
- Click cards to navigate to filtered pages

## Data Flow Patterns

### Create Operation Flow
```
User Input → Pydantic Validation → MongoDB Insert → Serialize → JSON Response
```

### Read Operation Flow
```
MongoDB Query → Serialize ObjectIds → Filter/Transform → JSON/HTML Response
```

### Update Operation Flow
```
User Input → Validate ID → MongoDB Update → Fetch Updated → Serialize → Response
```

### Delete Operation Flow
```
Validate ID → MongoDB Delete → Verify Deletion → Success Response
```

## Error Handling Workflow

1. **Database Connection Errors:**
   - Check if `db is None`
   - Return 500 with descriptive error message
   - User sees error on frontend

2. **Validation Errors:**
   - Pydantic models validate input
   - Invalid data returns 422 with validation details
   - Frontend displays validation errors

3. **Not Found Errors:**
   - Check if document exists in MongoDB
   - Return 404 with "X not found" message
   - Frontend handles gracefully

4. **Invalid ID Format:**
   - Try to convert string to ObjectId
   - Catch exception, return 400
   - User sees "Invalid ID format" message

## Frontend-Backend Communication

### API Endpoints (JSON)
- All `/api/*` routes return JSON
- Used by frontend JavaScript for dynamic updates
- Support filtering via query parameters

### Page Routes (HTML)
- All page routes return rendered HTML templates
- Use Jinja2 templating for server-side rendering
- Include data directly in template context

### AJAX Requests
- Frontend uses `fetch()` for API calls
- Updates DOM without page refresh
- Handles errors with user-friendly messages

## State Management

- **Server-Side State**: MongoDB database
- **Client-Side State**: JavaScript variables, DOM
- **No Session Management**: Stateless API design
- **Filter State**: URL query parameters for navigation

## Concurrent Operations

- Multiple users can access system simultaneously
- MongoDB handles concurrent reads/writes
- No locking mechanism (optimistic updates)
- Last write wins for updates


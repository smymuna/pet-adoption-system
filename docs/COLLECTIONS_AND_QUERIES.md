# Collections and Queries - MongoDB Schema

## Database Structure

**Database Name**: `pet_adoption`

## Collections Overview

### 1. `animals` Collection

**Purpose**: Stores all animal records in the shelter

**Schema**:
```javascript
{
  _id: ObjectId,
  name: String,                    // Required
  species: String,                 // Required (Dog, Cat, Rabbit, etc.)
  breed: String,                   // Optional
  age: Number,                     // Required (> 0)
  gender: String,                  // Required (Male, Female)
  status: String,                  // Required (Available, Adopted, Medical)
  intake_date: String,             // Optional (YYYY-MM-DD)
  behavioral_notes: String,        // Optional
  assigned_volunteers: [String]    // Array of volunteer ObjectId strings
}
```

**Common Queries**:
```python
# Get all animals
db.animals.find()

# Get available animals
db.animals.find({'status': 'Available'})

# Get animals by species
db.animals.find({'species': 'Dog'})

# Get animals with assigned volunteers
db.animals.find({'assigned_volunteers': {'$exists': True, '$ne': []}})

# Get animals needing volunteers (available but no volunteers)
db.animals.find({
    'status': 'Available',
    '$or': [
        {'assigned_volunteers': {'$exists': False}},
        {'assigned_volunteers': []}
    ]
})

# Find animal by ID
db.animals.find_one({'_id': ObjectId(animal_id)})

# Update animal status
db.animals.update_one(
    {'_id': ObjectId(animal_id)},
    {'$set': {'status': 'Adopted'}}
)

# Add volunteer to animal
db.animals.update_one(
    {'_id': ObjectId(animal_id)},
    {'$addToSet': {'assigned_volunteers': volunteer_id_str}}
)

# Remove volunteer from animal
db.animals.update_one(
    {'_id': ObjectId(animal_id)},
    {'$pull': {'assigned_volunteers': volunteer_id_str}}
)
```

**Indexes** (recommended):
- `{'species': 1}`
- `{'status': 1}`
- `{'assigned_volunteers': 1}`

---

### 2. `adopters` Collection

**Purpose**: Stores information about people who adopt animals

**Schema**:
```javascript
{
  _id: ObjectId,
  name: String,        // Required
  phone: String,       // Required
  email: String,       // Required (validated email)
  address: String      // Required
}
```

**Common Queries**:
```python
# Get all adopters
db.adopters.find()

# Find adopter by ID
db.adopters.find_one({'_id': ObjectId(adopter_id)})

# Search adopters by name (if needed)
db.adopters.find({'name': {'$regex': search_term, '$options': 'i'}})
```

---

### 3. `adoptions` Collection

**Purpose**: Links animals to adopters, records adoption history

**Schema**:
```javascript
{
  _id: ObjectId,
  animal_id: ObjectId,      // Reference to animals._id
  adopter_id: ObjectId,     // Reference to adopters._id
  adoption_date: String,    // YYYY-MM-DD format
  notes: String             // Optional
}
```

**Common Queries**:
```python
# Get all adoptions
db.adoptions.find()

# Get adoptions by adopter
db.adoptions.find({'adopter_id': ObjectId(adopter_id)})

# Get adoptions by animal
db.adoptions.find({'animal_id': ObjectId(animal_id)})

# Get adoptions in date range
db.adoptions.find({
    'adoption_date': {
        '$gte': start_date,
        '$lte': end_date
    }
})

# Get monthly adoption counts (aggregation)
db.adoptions.aggregate([
    {'$group': {
        '_id': {'$substr': ['$adoption_date', 0, 7]},  # YYYY-MM
        'count': {'$sum': 1}
    }},
    {'$sort': {'_id': 1}}
])
```

**Relationships**:
- `animal_id` → `animals._id`
- `adopter_id` → `adopters._id`

---

### 4. `medical_records` Collection

**Purpose**: Tracks veterinary visits and medical history

**Schema**:
```javascript
{
  _id: ObjectId,
  animal_id: ObjectId,      // Reference to animals._id
  vet_name: String,         // Required
  visit_date: String,       // Required (YYYY-MM-DD)
  diagnosis: String,        // Required
  treatment: String,        // Required
  notes: String            // Optional
}
```

**Common Queries**:
```python
# Get all medical records
db.medical_records.find()

# Get records for specific animal
db.medical_records.find({'animal_id': ObjectId(animal_id)})

# Get records sorted by date (newest first)
db.medical_records.find({'animal_id': ObjectId(animal_id)}).sort('visit_date', -1)

# Get records in date range
db.medical_records.find({
    'visit_date': {
        '$gte': start_date,
        '$lte': end_date
    }
})

# Get medical visits by species (aggregation)
db.medical_records.aggregate([
    {'$lookup': {
        'from': 'animals',
        'localField': 'animal_id',
        'foreignField': '_id',
        'as': 'animal_info'
    }},
    {'$unwind': '$animal_info'},
    {'$group': {
        '_id': '$animal_info.species',
        'count': {'$sum': 1}
    }},
    {'$sort': {'count': -1}}
])

# Get medical visits by breed (aggregation)
db.medical_records.aggregate([
    {'$lookup': {
        'from': 'animals',
        'localField': 'animal_id',
        'foreignField': '_id',
        'as': 'animal_info'
    }},
    {'$unwind': '$animal_info'},
    {'$match': {'animal_info.species': species}},
    {'$group': {
        '_id': '$animal_info.breed',
        'count': {'$sum': 1}
    }},
    {'$sort': {'count': -1}}
])
```

**Relationships**:
- `animal_id` → `animals._id`

---

### 5. `volunteers` Collection

**Purpose**: Manages volunteer information and skills

**Schema**:
```javascript
{
  _id: ObjectId,
  name: String,            // Required
  phone: String,           // Required
  email: String,           // Required (validated email)
  skills: [String],       // Array of skill names (standardized)
  availability: String     // Required (Weekdays, Weekends, Flexible, etc.)
}
```

**Common Queries**:
```python
# Get all volunteers
db.volunteers.find()

# Get volunteers with specific skill
db.volunteers.find({'skills': 'Dog Walking'})

# Get volunteers with multiple skills
db.volunteers.find({'skills': {'$in': ['Dog Walking', 'Grooming']}})

# Find volunteer by ID
db.volunteers.find_one({'_id': ObjectId(volunteer_id)})

# Get volunteers for species (skill-based matching)
# Skills matched via backend/volunteer_skills.py
matching_skills = get_skills_for_species('Dog')
# Returns: ['Dog Walking', 'Dog Training', 'Grooming', ...]
db.volunteers.find({'skills': {'$in': matching_skills}})
```

**Standardized Skills** (from `backend/volunteer_skills.py`):
- Dog Walking, Dog Training, Cat Socialization
- Small Animal Care, Bird Care
- Grooming, Feeding, Medical Assistance
- Adoption Events, Meet & Greets
- Photography, Social Media, Administrative
- Cleaning, Transportation
- Behavioral Assessment
- Senior Animal Care, Puppy/Kitten Care

---

### 6. `volunteer_activities` Collection

**Purpose**: Logs volunteer work with animals, tracks hours

**Schema**:
```javascript
{
  _id: ObjectId,
  volunteer_id: ObjectId,      // Reference to volunteers._id
  animal_id: ObjectId,         // Reference to animals._id
  activity_type: String,        // Walking, Feeding, Grooming, etc.
  activity_date: String,        // YYYY-MM-DD
  duration_minutes: Number,     // Required (> 0)
  notes: String                // Optional
}
```

**Common Queries**:
```python
# Get all activities
db.volunteer_activities.find()

# Get activities by volunteer
db.volunteer_activities.find({'volunteer_id': volunteer_id_str})

# Get activities by animal
db.volunteer_activities.find({'animal_id': animal_id_str})

# Get activities sorted by date
db.volunteer_activities.find().sort('activity_date', -1)

# Calculate total volunteer hours
total_hours = 0
for activity in db.volunteer_activities.find():
    total_hours += activity.get('duration_minutes', 0) / 60.0

# Get activities by type (aggregation)
db.volunteer_activities.aggregate([
    {'$group': {
        '_id': '$activity_type',
        'count': {'$sum': 1},
        'total_minutes': {'$sum': '$duration_minutes'}
    }},
    {'$sort': {'count': -1}}
])

# Get top volunteers by hours (aggregation)
db.volunteer_activities.aggregate([
    {'$group': {
        '_id': '$volunteer_id',
        'total_minutes': {'$sum': '$duration_minutes'},
        'activity_count': {'$sum': 1}
    }},
    {'$lookup': {
        'from': 'volunteers',
        'localField': '_id',
        'foreignField': '_id',
        'as': 'volunteer_info'
    }},
    {'$unwind': '$volunteer_info'},
    {'$project': {
        'volunteer_name': '$volunteer_info.name',
        'total_hours': {'$divide': ['$total_minutes', 60]},
        'activity_count': 1
    }},
    {'$sort': {'total_hours': -1}},
    {'$limit': 10}
])
```

**Relationships**:
- `volunteer_id` → `volunteers._id`
- `animal_id` → `animals._id`

---

## Complex Queries & Aggregations

### 1. Adoption Rate by Species

```python
# Get adopted count per species
adopted = db.animals.aggregate([
    {'$match': {'status': 'Adopted'}},
    {'$group': {'_id': '$species', 'count': {'$sum': 1}}}
])

# Get available count per species
available = db.animals.aggregate([
    {'$match': {'status': 'Available'}},
    {'$group': {'_id': '$species', 'count': {'$sum': 1}}}
])

# Combine in Python
```

### 2. Monthly Adoptions with Filters

```python
pipeline = [
    {'$lookup': {
        'from': 'animals',
        'localField': 'animal_id',
        'foreignField': '_id',
        'as': 'animal_info'
    }},
    {'$unwind': '$animal_info'},
    {'$match': {
        'animal_info.species': species,  # If filter applied
        'adoption_date': {
            '$gte': start_date,
            '$lte': end_date
        }
    }},
    {'$group': {
        '_id': {'$substr': ['$adoption_date', 0, 7]},
        'count': {'$sum': 1}
    }},
    {'$sort': {'_id': 1}}
]
```

### 3. Medical Visits by Species with Animal Filters

```python
# First, get matching animals based on filters
animal_filter = {'species': 'Dog', 'status': 'Available'}
matching_animals = {str(a['_id']) for a in db.animals.find(animal_filter)}

# Then query medical records
pipeline = [
    {'$match': {
        'animal_id': {'$in': [ObjectId(aid) for aid in matching_animals]},
        'visit_date': {
            '$gte': start_date,
            '$lte': end_date
        }
    }},
    {'$lookup': {
        'from': 'animals',
        'localField': 'animal_id',
        'foreignField': '_id',
        'as': 'animal_info'
    }},
    {'$unwind': '$animal_info'},
    {'$group': {
        '_id': '$animal_info.species',
        'count': {'$sum': 1}
    }},
    {'$sort': {'count': -1}}
]
```

### 4. Suggested Volunteers for Animal

```python
# Get animal species
animal = db.animals.find_one({'_id': ObjectId(animal_id)})
species = animal['species']

# Get matching skills
matching_skills = get_skills_for_species(species)

# Find volunteers with matching skills
volunteers = db.volunteers.find({
    'skills': {'$in': matching_skills}
})

# Filter out already assigned
assigned = animal.get('assigned_volunteers', [])
suggested = [v for v in volunteers if str(v['_id']) not in assigned]

# Sort by number of matching skills
suggested.sort(key=lambda v: len(set(v['skills']) & set(matching_skills)), reverse=True)
```

## Query Performance Considerations

### Indexes to Add

```javascript
// Animals collection
db.animals.createIndex({species: 1})
db.animals.createIndex({status: 1})
db.animals.createIndex({assigned_volunteers: 1})
db.animals.createIndex({species: 1, status: 1})  // Compound index

// Adoptions collection
db.adoptions.createIndex({adopter_id: 1})
db.adoptions.createIndex({animal_id: 1})
db.adoptions.createIndex({adoption_date: 1})

// Medical records collection
db.medical_records.createIndex({animal_id: 1})
db.medical_records.createIndex({visit_date: 1})

// Volunteer activities collection
db.volunteer_activities.createIndex({volunteer_id: 1})
db.volunteer_activities.createIndex({animal_id: 1})
db.volunteer_activities.createIndex({activity_date: -1})
```

### Query Optimization Tips

1. **Use Projection**: Only fetch needed fields
   ```python
   db.animals.find({}, {'name': 1, 'species': 1, 'status': 1})
   ```

2. **Limit Results**: Use `.limit()` for large datasets
   ```python
   db.animals.find().limit(100)
   ```

3. **Use Aggregation**: For complex calculations
   ```python
   # Instead of fetching all and counting in Python
   # Use $group in aggregation pipeline
   ```

4. **Batch Operations**: Use `insert_many()` for multiple inserts
   ```python
   db.animals.insert_many([animal1, animal2, animal3])
   ```

## Data Relationships Summary

```
animals (1) ──→ (many) adoptions ──→ (1) adopters
  │
  ├──→ (many) medical_records
  │
  └──→ (many) volunteer_activities ──→ (1) volunteers
```

**Key Points**:
- One animal can have many adoptions (if returned)
- One animal can have many medical records
- One animal can have many volunteer activities
- One volunteer can have many activities
- Many-to-many: animals ↔ volunteers (via assigned_volunteers array)


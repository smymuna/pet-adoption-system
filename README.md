# Pet Adoption & Animal Shelter Management System (PASMS)

A complete full-stack web application built with **FastAPI**, **MongoDB**, **HTML/CSS/JS**, and **Bootstrap 5 Admin Dashboard** with data visualization.

## 🚀 Features

- ✅ **Full CRUD operations** for 6 collections (Animals, Adopters, Adoptions, Medical Records, Volunteers, Volunteer Activities)
- ✅ **Search functionality** (by adopter, medical records)
- ✅ **Advanced data visualization** with Chart.js:
  - Species & Breed distribution
  - Status, Age, and Gender distribution
  - Monthly adoption trends
  - Adoption rate by species
  - Medical visits over time
  - Medical visits by species and breed
  - **Comprehensive filtering** (species, status, gender, breed, date range)
- ✅ **Volunteer Management System**:
  - Assign/unassign volunteers to animals
  - Skill-based volunteer matching
  - Volunteer activity logging
  - Volunteer statistics and analytics
  - Standardized skills system (18 skill types)
- ✅ **Bootstrap 5 Admin Dashboard** with responsive sidebar navigation
- ✅ **Automatic API documentation** (Swagger UI & ReDoc)
- ✅ **Interactive filtering** on all charts and animal listings

## 📁 Project Structure

```
pet-adoption-system/
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .env                         # Environment variables (create from .env.example)
│
├── backend/                     # 🖥️ BACKEND - Server-side code
│   ├── config.py               # Configuration (MongoDB connection)
│   ├── models.py               # Pydantic data models
│   ├── api/routes/             # API route handlers
│   │   ├── dashboard.py
│   │   ├── animals.py
│   │   ├── adopters.py
│   │   ├── adoptions.py
│   │   ├── medical.py
│   │   ├── volunteers.py
│   │   ├── volunteer_activities.py
│   │   ├── search.py
│   │   └── charts.py
│   ├── species_breeds.py    # Species and breed definitions
│   └── volunteer_skills.py  # Volunteer skills definitions
│   └── database/
│       └── connection.py       # MongoDB connection management
│
├── frontend/                    # 🎨 FRONTEND - Client-side code
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── animals.html
│   │   ├── adopters.html
│   │   ├── adoptions.html
│   │   ├── medical.html
│   │   ├── volunteers.html
│   │   ├── volunteer_activities.html
│   │   ├── search_adopter.html
│   │   ├── search_medical.html
│   │   └── charts.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── scripts.js
│
├── utils/                       # 🛠️ UTILITIES
│   ├── add_sample_data.py      # Add sample data to database
│   └── test_mongodb_connection.py  # Test MongoDB connection
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install and Start MongoDB

**On macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**On Windows:**
Download and install from [MongoDB Download Center](https://www.mongodb.com/try/download/community)

### 3. Configure MongoDB Connection (Optional)

If you need to customize the connection, create a `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=pet_adoption
```

**Default values:**
- `MONGO_URI`: `mongodb://localhost:27017/` (local MongoDB)
- `DB_NAME`: `pet_adoption`

### 4. Test Connection
```bash
python utils/test_mongodb_connection.py
```

### 5. Add Sample Data (Optional)

```bash
python utils/add_sample_data.py
```

### 6. Run the Application

**Development mode:**
```bash
python main.py
```

**Or using uvicorn directly:**
```bash
uvicorn main:app --reload --port 5001
```

## 🌐 Access Points

- **Web Interface**: http://localhost:5001
- **API Documentation**: http://localhost:5001/docs (Swagger UI)
- **Alternative Docs**: http://localhost:5001/redoc (ReDoc)

## 📈 Key Features Details

### Data Visualization & Analytics
- **10+ Interactive Charts** with real-time filtering
- **Filter Support**: All charts support filtering by species, status, gender, breed, and date range
- **Chart Types**: Pie, Doughnut, Bar, Line charts
- **Organized Sections**: Animal Demographics, Adoption Analytics, Medical Analytics

### Volunteer Management
- **Skill-Based Matching**: Automatically suggests volunteers based on animal species and volunteer skills
- **Activity Tracking**: Log volunteer activities (walking, feeding, grooming, training, etc.)
- **Statistics Dashboard**: View volunteer hours, top volunteers, activity breakdowns
- **Assignment Management**: Easy assign/unassign with visual indicators

### Advanced Filtering
- **Universal Filters**: Apply filters across all charts simultaneously
- **Dynamic Dropdowns**: Breed dropdown updates based on selected species
- **Date Range Filtering**: Filter time-based charts by date ranges
- **URL Parameters**: Navigate with pre-applied filters (e.g., `/animals?status=Available`)

## 📊 MongoDB Collections Schema

### animals
- `_id` (ObjectId)
- `name` (String)
- `species` (String)
- `breed` (String, optional)
- `age` (Number)
- `gender` (String: Male, Female)
- `status` (String: Available, Adopted, Medical)
- `intake_date` (String, optional: YYYY-MM-DD)
- `behavioral_notes` (String, optional)
- `assigned_volunteers` (Array of ObjectId strings, optional)

### adopters
- `_id` (ObjectId)
- `name` (String)
- `phone` (String)
- `email` (String)
- `address` (String)

### adoptions
- `_id` (ObjectId)
- `animal_id` (ObjectId)
- `adopter_id` (ObjectId)
- `adoption_date` (String: YYYY-MM-DD)
- `notes` (String, optional)

### medical_records
- `_id` (ObjectId)
- `animal_id` (ObjectId)
- `vet_name` (String)
- `visit_date` (String: YYYY-MM-DD)
- `diagnosis` (String)
- `treatment` (String)
- `notes` (String, optional)

### volunteers
- `_id` (ObjectId)
- `name` (String)
- `phone` (String)
- `email` (String)
- `skills` (Array of Strings) - Standardized skills from volunteer_skills.py
- `availability` (String)

### volunteer_activities
- `_id` (ObjectId)
- `volunteer_id` (ObjectId)
- `animal_id` (ObjectId)
- `activity_type` (String: Walking, Feeding, Grooming, Training, etc.)
- `activity_date` (String: YYYY-MM-DD)
- `duration_minutes` (Number)
- `notes` (String, optional)

## 🔧 Troubleshooting

### MongoDB Connection Issues

1. **Check MongoDB service**: Ensure MongoDB is running locally
   - macOS: `brew services list` (should show mongodb-community as started)
   - Linux: `sudo systemctl status mongodb`
   - Windows: Check Services panel for MongoDB service

2. **Default connection**: The app uses `mongodb://localhost:27017/` by default
   - If MongoDB runs on a different port, set `MONGO_URI` in `.env`

3. **Test connection**: Run `python utils/test_mongodb_connection.py`

4. **Start MongoDB manually** (if service not running):
   - macOS: `brew services start mongodb-community`
   - Linux: `sudo systemctl start mongodb`
   - Or run directly: `mongod --dbpath /path/to/data`

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


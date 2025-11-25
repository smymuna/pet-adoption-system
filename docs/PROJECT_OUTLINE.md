# Pet Adoption & Animal Shelter Management System (PASMS)
## Project Outline, Tech Stack & Approach

---

## 📋 Project Overview

**Pet Adoption & Animal Shelter Management System (PASMS)** is a comprehensive full-stack web application designed to help animal shelters manage their operations efficiently. The system provides complete CRUD operations for managing animals, adopters, adoptions, medical records, and volunteers, along with advanced analytics, data visualization, and machine learning-powered adoption predictions.

### Core Purpose
- Streamline shelter operations and record-keeping
- Improve adoption rates through data-driven insights
- Predict adoption likelihood and time-to-adoption using ML
- Provide actionable analytics for shelter management
- Track medical history and volunteer activities

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: FastAPI 0.104.1
  - Modern, fast Python web framework
  - Automatic API documentation (Swagger UI & ReDoc)
  - Built-in data validation with Pydantic
  - Async/await support for high performance

- **Server**: Uvicorn
  - ASGI server for FastAPI
  - Hot reload for development

- **Database**: MongoDB
  - NoSQL document database
  - Flexible schema for evolving data models
  - Local MongoDB instance (default: `mongodb://localhost:27017/`)
  - PyMongo 4.6.0 for database operations

- **Data Validation**: Pydantic 2.9.0+
  - Type-safe data models
  - Automatic validation and serialization
  - Email validation support

### **Frontend**
- **Templating**: Jinja2 3.1.2
  - Server-side rendering
  - Template inheritance
  - Dynamic content generation

- **UI Framework**: Bootstrap 5.3.0
  - Responsive design
  - Modern admin dashboard layout
  - Pre-built components and utilities

- **Icons**: Bootstrap Icons 1.10.0
  - Comprehensive icon library
  - Consistent visual language

- **Charts & Visualization**: Chart.js 4.4.0
  - Interactive charts and graphs
  - Multiple chart types (bar, line, pie, doughnut)
  - Responsive and customizable

- **JavaScript**: Vanilla ES6+
  - No framework dependencies
  - Modern async/await patterns
  - Fetch API for HTTP requests

### **Machine Learning**
- **Library**: scikit-learn 1.4.0+
  - Random Forest Classifier (adoption likelihood)
  - Random Forest Regressor (time-to-adoption)
  - Label encoding for categorical features
  - Model persistence with joblib

- **Data Processing**: 
  - Pandas 2.2.0+ for data manipulation
  - NumPy 1.26.0+ for numerical operations

### **Development Tools**
- **Testing**: pytest 7.4.3
  - Unit tests
  - Integration tests
  - Test coverage reporting

- **Environment Management**: python-dotenv 1.0.0
  - Secure configuration management
  - Environment variable handling

---

## 🏗️ Architecture & Approach

### **Architecture Pattern**
**Layered Architecture (3-Tier)**
```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│  (HTML Templates, CSS, JavaScript)  │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│         Application Layer           │
│  (FastAPI Routes, Business Logic)   │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│         Data Layer                   │
│  (MongoDB, ML Models, Data Access)  │
└─────────────────────────────────────┘
```

### **Project Structure**
```
pet-adoption-system/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python runtime version
├── pytest.ini                # Test configuration
│
├── backend/                  # Backend application
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic data models
│   ├── species_breeds.py     # Species/breed definitions
│   │
│   ├── api/                 # API routes
│   │   ├── routes/
│   │   │   ├── dashboard.py      # Dashboard statistics
│   │   │   ├── animals.py        # Animal CRUD operations
│   │   │   ├── adopters.py       # Adopter management
│   │   │   ├── adoptions.py      # Adoption tracking
│   │   │   ├── medical.py        # Medical records
│   │   │   ├── volunteers.py     # Volunteer management
│   │   │   ├── search.py         # Search functionality
│   │   │   ├── charts.py          # Data visualization APIs
│   │   │   └── ml_predictions.py # ML prediction endpoints
│   │
│   └── database/
│       └── connection.py    # MongoDB connection management
│
├── frontend/                 # Frontend application
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template with sidebar
│   │   ├── dashboard.html   # Main dashboard
│   │   ├── animals.html     # Animal management
│   │   ├── adopters.html    # Adopter management
│   │   ├── adoptions.html   # Adoption tracking
│   │   ├── medical.html     # Medical records
│   │   ├── volunteers.html  # Volunteer management
│   │   ├── search_adopter.html
│   │   ├── search_medical.html
│   │   ├── charts.html      # Data visualization
│   │   └── ml_predictions.html # ML predictions
│   │
│   └── static/              # Static assets
│       ├── css/
│       │   └── style.css     # Custom styles
│       └── js/
│           └── scripts.js   # Shared JavaScript utilities
│
├── ml/                      # Machine Learning
│   ├── models.py           # ML model training & prediction
│   └── saved_models/       # Trained model files (.pkl)
│
├── utils/                   # Utility scripts
│   ├── add_sample_data.py  # Sample data generator
│   └── test_mongodb_connection.py # Connection testing
│
└── tests/                   # Test suite
    ├── unit/               # Unit tests
    ├── integration/        # Integration tests
    └── conftest.py        # Test configuration
```

---

## 🎯 Development Approach

### **1. API-First Design**
- RESTful API endpoints for all operations
- Separate API routes from page routes
- JSON responses for programmatic access
- HTML responses for web interface
- Automatic API documentation via Swagger

### **2. Data Modeling**
- **Pydantic Models**: Type-safe request/response validation
- **MongoDB Collections**: Flexible document structure
- **Schema Evolution**: Backward-compatible field additions
- **Data Validation**: Automatic validation at API boundaries

### **3. Machine Learning Integration**
- **Feature Engineering**: 
  - Species, breed, age, gender, status
  - Days in shelter (calculated from intake_date)
  - Medical history count
- **Model Training**: On-demand training with data validation
- **Prediction Pipeline**: Real-time predictions for available animals
- **Feature Importance**: Transparent model interpretability

### **4. User Experience**
- **Progressive Enhancement**: Works without JavaScript for basic operations
- **Responsive Design**: Mobile-friendly Bootstrap layout
- **Interactive Elements**: Dynamic forms, real-time updates
- **Visual Feedback**: Loading states, success/error messages
- **Accessibility**: Semantic HTML, ARIA labels

### **5. Code Organization**
- **Separation of Concerns**: Routes, models, database logic separated
- **Reusable Components**: Shared utilities and templates
- **Configuration Management**: Environment-based configuration
- **Error Handling**: Comprehensive error handling and user feedback

---

## 🔑 Key Features

### **Core Features**
1. **Animal Management**
   - Full CRUD operations
   - Species/breed categorization (10+ species, 100+ breeds)
   - Intake date tracking
   - Status management (Available, Adopted, Medical)

2. **Adoption Tracking**
   - Link animals to adopters
   - Adoption date recording
   - Adoption notes and history

3. **Medical Records**
   - Vet visit tracking
   - Diagnosis and treatment records
   - Medical history per animal

4. **Adopter Management**
   - Contact information
   - Adoption history
   - Search functionality

5. **Volunteer Management**
   - Skills and availability tracking
   - Contact management

### **Advanced Features**
1. **Data Visualization**
   - Species distribution charts
   - Status distribution
   - Age distribution
   - Gender distribution
   - Monthly adoption trends
   - Adoption rate by species
   - Medical visits over time
   - **Filtering**: By species, status, gender, date range

2. **Machine Learning Predictions**
   - **Adoption Likelihood**: Probability (0-100%) that an animal will be adopted
   - **Time-to-Adoption**: Predicted days until adoption
   - **Feature Importance**: Shows which factors matter most
   - **7 Features**: Species, breed, age, gender, status, days in shelter, medical count

3. **Search & Filtering**
   - Search by adopter
   - Search medical records
   - Filter charts by multiple criteria

---

## 📊 Data Models

### **Animals Collection**
```python
{
    "_id": ObjectId,
    "name": str,
    "species": str,              # Dog, Cat, Rabbit, Bird, etc.
    "breed": str (optional),     # Labrador, Persian, etc.
    "age": int,                  # Years
    "gender": str,               # Male, Female
    "status": str,               # Available, Adopted, Medical
    "intake_date": str (optional) # YYYY-MM-DD format
}
```

### **Adopters Collection**
```python
{
    "_id": ObjectId,
    "name": str,
    "phone": str,
    "email": EmailStr,
    "address": str
}
```

### **Adoptions Collection**
```python
{
    "_id": ObjectId,
    "animal_id": ObjectId,
    "adopter_id": ObjectId,
    "adoption_date": str,        # YYYY-MM-DD
    "notes": str (optional)
}
```

### **Medical Records Collection**
```python
{
    "_id": ObjectId,
    "animal_id": ObjectId,
    "vet_name": str,
    "visit_date": str,           # YYYY-MM-DD
    "diagnosis": str,
    "treatment": str,
    "notes": str (optional)
}
```

### **Volunteers Collection**
```python
{
    "_id": ObjectId,
    "name": str,
    "phone": str,
    "email": EmailStr,
    "skills": str,
    "availability": str
}
```

---

## 🤖 Machine Learning Approach

### **Model Architecture**
- **Algorithm**: Random Forest (Ensemble Learning)
- **Adoption Likelihood**: RandomForestClassifier (Binary Classification)
- **Time-to-Adoption**: RandomForestRegressor (Regression)

### **Feature Set**
**Adoption Likelihood (7 features):**
1. Species (encoded)
2. Breed (encoded)
3. Age (numeric)
4. Gender (encoded)
5. Status (encoded)
6. Days in Shelter (calculated)
7. Medical History Count (numeric)

**Time-to-Adoption (6 features):**
1. Species (encoded)
2. Breed (encoded)
3. Age (numeric)
4. Gender (encoded)
5. Days in Shelter (numeric)
6. Medical History Count (numeric)

### **Training Process**
1. Data preparation from MongoDB collections
2. Feature encoding (LabelEncoder for categorical)
3. Train/test split (80/20)
4. Model training with 100 estimators
5. Model evaluation (accuracy/R² score)
6. Model persistence (joblib)
7. Feature importance extraction

### **Prediction Workflow**
1. Load trained models
2. Encode input features
3. Calculate derived features (days in shelter, medical count)
4. Generate predictions
5. Return probabilities/estimates with feature importance

---

## 🔄 Development Workflow

### **Local Development**
1. Install dependencies: `pip install -r requirements.txt`
2. Install and start MongoDB locally (default: `mongodb://localhost:27017/`)
3. (Optional) Configure MongoDB: Set `MONGO_URI` in `.env` if using custom settings
4. Run development server: `python main.py` or `uvicorn main:app --reload`
5. Access application: `http://localhost:5001`

### **Testing**
- Unit tests: `pytest tests/unit/`
- Integration tests: `pytest tests/integration/`
- Full test suite: `pytest tests/`

---

## 📈 Future Enhancements

### **Planned Features**
1. Enhanced dashboard with real-time metrics
2. Advanced search and filtering on all pages
3. Data export (CSV/Excel)
4. Photo upload for animals
5. Email notifications and alerts
6. Adoption workflow management
7. Bulk data import
8. Advanced analytics and reporting
9. Mobile app API
10. User authentication and roles

---

## 🎓 Best Practices Implemented

1. **Type Safety**: Pydantic models for validation
2. **Error Handling**: Comprehensive try-catch blocks
3. **Code Reusability**: Shared utilities and templates
4. **Documentation**: Inline comments and docstrings
5. **Testing**: Unit and integration tests
6. **Security**: Environment-based configuration
7. **Performance**: Async operations, efficient queries
8. **Maintainability**: Clear structure, separation of concerns
9. **Scalability**: Stateless API design
10. **User Experience**: Responsive, intuitive interface

---

## 📝 Summary

**PASMS** is a modern, full-stack web application built with Python/FastAPI and MongoDB, featuring:
- Complete shelter management functionality
- Advanced data visualization with filtering
- Machine learning-powered adoption predictions
- Clean, maintainable codebase
- Scalable architecture

The system demonstrates best practices in web development, data science, and software engineering, providing a solid foundation for animal shelter operations management.


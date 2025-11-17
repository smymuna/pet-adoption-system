# Pet Adoption & Animal Shelter Management System (PASMS)

A complete full-stack web application built with **FastAPI**, **MongoDB**, **HTML/CSS/JS**, and **Bootstrap 5 Admin Dashboard** with **Machine Learning** predictions.

## 🚀 Features

- ✅ **Full CRUD operations** for 5 collections (Animals, Adopters, Adoptions, Medical Records, Volunteers)
- ✅ **Search functionality** (by adopter, medical records)
- ✅ **Data visualization** with Chart.js (Species distribution, Monthly adoptions)
- ✅ **Machine Learning** predictions (Adoption likelihood, Time-to-adoption)
- ✅ **Bootstrap 5 Admin Dashboard** with responsive sidebar navigation
- ✅ **Automatic API documentation** (Swagger UI & ReDoc)

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
│   │   ├── search.py
│   │   ├── charts.py
│   │   └── ml_predictions.py
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
│   │   ├── search_adopter.html
│   │   ├── search_medical.html
│   │   ├── charts.html
│   │   └── ml_predictions.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── scripts.js
│
├── ml/                          # 🤖 MACHINE LEARNING
│   ├── models.py               # ML model training & prediction
│   └── saved_models/           # Trained models (.pkl files)
│
├── utils/                       # 🛠️ UTILITIES
│   ├── add_sample_data.py      # Add sample data to database
│   ├── keep_mongodb_alive.py   # Keep MongoDB cluster active
│   └── test_mongodb_connection.py  # Test MongoDB connection
│
└── docs/                        # 📚 DOCUMENTATION
    └── MONGODB_SETUP.md        # MongoDB Atlas setup guide
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB

1. Create `.env` file (if not exists):
   ```bash
   # Copy from .env.example if available
   ```

2. Edit `.env` and add your MongoDB Atlas connection string:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

3. Test connection:
   ```bash
   python utils/test_mongodb_connection.py
   ```

### 3. Add Sample Data (Optional)

```bash
python utils/add_sample_data.py
```

### 4. Run the Application

**Development mode:**
```bash
python main.py
```

**Or using uvicorn directly:**
```bash
uvicorn main:app --reload --port 5001
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 5001 --workers 4
```

## 🌐 Access Points

- **Web Interface**: http://localhost:5001
- **API Documentation**: http://localhost:5001/docs (Swagger UI)
- **Alternative Docs**: http://localhost:5001/redoc (ReDoc)

## 📊 MongoDB Collections Schema

### animals
- `_id` (ObjectId)
- `name` (String)
- `species` (String)
- `age` (Number)
- `gender` (String: Male, Female)
- `status` (String: Available, Adopted, Medical)

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
- `skills` (String)
- `availability` (String)

## 🤖 Machine Learning Features

The system includes two ML models:

1. **Adoption Likelihood Prediction**: Predicts the probability that an animal will be adopted
2. **Time-to-Adoption Prediction**: Predicts how many days until an animal is adopted

To train the models:
1. Ensure you have sufficient data (at least 10 animals for likelihood, 5 adoptions for time-to-adoption)
2. Navigate to the ML Predictions page
3. Click "Train Models"
4. Click "Refresh Predictions" to see predictions

## 🔧 Troubleshooting

### MongoDB Connection Issues

1. **Check cluster status**: Ensure your MongoDB Atlas cluster is running (not paused)
2. **Network access**: Verify your IP is whitelisted in MongoDB Atlas
3. **Connection string**: Ensure your MONGO_URI in `.env` is correct
4. **Test connection**: Run `python utils/test_mongodb_connection.py`

### Keep MongoDB Active (Free Tier)

MongoDB Atlas free tier clusters auto-pause after inactivity. To prevent this:

```bash
python utils/keep_mongodb_alive.py
```

This script will ping MongoDB every 30 minutes to keep it active.

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


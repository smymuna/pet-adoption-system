# Pet Adoption & Animal Shelter Management System (PASMS)

A complete full-stack web application built with **FastAPI**, **MongoDB**, **HTML/CSS/JS**, and **Bootstrap 5 Admin Dashboard** with data visualization.

## 🚀 Features

- ✅ **Full CRUD operations** for 5 collections (Animals, Adopters, Adoptions, Medical Records, Volunteers)
- ✅ **Search functionality** (by adopter, medical records)
- ✅ **Data visualization** with Chart.js (Species distribution, Monthly adoptions, Age/Gender distribution)
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
│   │   └── charts.py
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


# Deployment Guide - MongoDB Atlas App Services (A2)

## 🚀 Deploying to MongoDB Atlas App Services

MongoDB Atlas App Services (formerly Realm) allows you to deploy serverless functions and HTTP endpoints directly connected to your MongoDB Atlas database.

## Prerequisites

1. **MongoDB Atlas Account** (you already have this)
2. **Atlas App Services enabled** on your cluster
3. **GitHub account** (for code deployment)

---

## Step-by-Step Deployment

### Step 1: Enable Atlas App Services

1. **Go to MongoDB Atlas:**
   - Log in to [cloud.mongodb.com](https://cloud.mongodb.com)
   - Select your cluster

2. **Enable App Services:**
   - Click on "App Services" in the left sidebar
   - Click "Create a New App"
   - Choose "Build your own App"
   - Name it: `pet-adoption-system`
   - Link it to your existing cluster
   - Click "Create App"

### Step 2: Configure App Services

1. **Set up Authentication (Optional):**
   - Go to "Authentication" in the left sidebar
   - Enable "Anonymous" authentication for public access
   - Or set up API Key authentication

2. **Configure Data Access:**
   - Go to "Data Access" → "Rules"
   - Set rules for your collections:
     ```json
     {
       "animals": {
         "read": true,
         "write": true
       },
       "adopters": {
         "read": true,
         "write": true
       },
       "adoptions": {
         "read": true,
         "write": true
       },
       "medical_records": {
         "read": true,
         "write": true
       },
       "volunteers": {
         "read": true,
         "write": true
       }
     }
     ```

### Step 3: Deploy HTTP Endpoints

**Note:** Atlas App Services uses serverless functions, not full FastAPI apps. You'll need to create individual HTTP endpoints for each route.

#### Option A: Deploy as Serverless Functions

1. **Go to "Functions" in App Services**

2. **Create HTTP Endpoint Functions:**
   - For each API route, create a function
   - Example for `get_animals`:
   ```javascript
   exports = async function(httpRequest, httpResponse) {
     const collection = context.services
       .get("mongodb-atlas")
       .db("pet_adoption")
       .collection("animals");
     
     const animals = await collection.find({}).toArray();
     
     return {
       statusCode: 200,
       headers: { "Content-Type": "application/json" },
       body: JSON.stringify(animals)
     };
   };
   ```

#### Option B: Deploy Full FastAPI App (Recommended)

Since Atlas App Services has limitations for full FastAPI apps, I recommend using **Render** or **Railway** instead, which are better suited for FastAPI.

However, if you want to use Atlas App Services, you can:

1. **Use Atlas HTTP Endpoints:**
   - Create HTTP endpoints that call your FastAPI app deployed elsewhere
   - Use Atlas as a proxy/API gateway

2. **Deploy FastAPI separately:**
   - Deploy FastAPI to Render/Railway
   - Use Atlas App Services for database triggers and serverless functions
   - Connect them together

---

## Alternative: Deploy to Render with MongoDB Atlas

Since FastAPI works better on traditional hosting, here's the recommended approach:

### Deploy FastAPI to Render + Use MongoDB Atlas Database

1. **Deploy FastAPI to Render:**
   - Follow the Render deployment guide in `DEPLOYMENT.md`
   - Use your existing MongoDB Atlas connection string
   - This gives you full FastAPI functionality

2. **Use Atlas App Services for:**
   - Database triggers (e.g., send email when animal is adopted)
   - Scheduled functions (e.g., daily reports)
   - Real-time sync (if needed)

---

## Recommended Deployment Strategy

For your Pet Adoption System, I recommend:

### Primary Deployment: Render or Railway
- Full FastAPI application
- All routes and features
- Easy to deploy and maintain

### Secondary: MongoDB Atlas App Services
- Database triggers
- Scheduled tasks
- Real-time notifications
- Background jobs

---

## Quick Deploy to Render (Easiest Option)

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** pet-adoption-system
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variable:
     - **Key:** `MONGO_URI`
     - **Value:** Your MongoDB Atlas connection string
   - Click "Create Web Service"

3. **Wait for deployment** (5-10 minutes)

4. **Access your app:**
   - Render provides a URL like: `https://pet-adoption-system.onrender.com`

---

## MongoDB Atlas Configuration for Deployment

1. **Network Access:**
   - Go to MongoDB Atlas → Network Access
   - Click "Add IP Address"
   - For Render: Add `0.0.0.0/0` (allow all) or Render's IP ranges
   - Click "Confirm"

2. **Database User:**
   - Ensure your database user has read/write permissions
   - Go to Database Access → Your User → Edit
   - Verify permissions

3. **Connection String:**
   - Go to Database → Connect → Drivers
   - Copy connection string
   - Replace `<password>` with your actual password
   - Use this in your deployment environment variables

---

## Need Help?

If you want to proceed with:
- **Render deployment** - I can guide you step-by-step
- **Atlas App Services** - I can help set up serverless functions
- **Both** - Deploy FastAPI to Render, use Atlas for triggers

Which would you like to do?


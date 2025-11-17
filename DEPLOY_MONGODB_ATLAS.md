# Deploy with MongoDB Atlas - Complete Guide

## 🎯 Deployment Strategy

Deploy your FastAPI app to **Render** (free tier) and connect it to your **existing MongoDB Atlas database**.

---

## ✅ Pre-Deployment Checklist

- [x] MongoDB Atlas cluster is set up
- [x] Connection string is ready
- [x] All code is ready
- [ ] Code pushed to GitHub
- [ ] MongoDB Atlas Network Access configured

---

## Step 1: Prepare Your Code

Your code is already ready! Just need to push to GitHub.

### 1.1 Initialize Git (if not done)

```bash
cd /Users/mona/pet-adoption-system
git init
git add .
git commit -m "Ready for deployment"
```

### 1.2 Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name: `pet-adoption-system`
4. Make it **Public** (for free Render tier) or Private
5. **Don't** initialize with README
6. Click "Create repository"

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/pet-adoption-system.git
git branch -M main
git push -u origin main
```

---

## Step 2: Configure MongoDB Atlas

### 2.1 Allow Network Access

1. Go to [cloud.mongodb.com](https://cloud.mongodb.com)
2. Select your cluster
3. Click **"Network Access"** in left sidebar
4. Click **"Add IP Address"**
5. Click **"Allow Access from Anywhere"** (adds 0.0.0.0/0)
   - Or add Render's specific IPs for better security
6. Click **"Confirm"**

### 2.2 Verify Database User

1. Go to **"Database Access"**
2. Ensure your user has:
   - **Read and write to any database** permissions
   - Or specific permissions to `pet_adoption` database

### 2.3 Get Connection String

1. Go to **"Database"** → Click **"Connect"**
2. Choose **"Drivers"**
3. Copy the connection string
4. Format: `mongodb+srv://admin:<password>@pets-db.qxoxk2g.mongodb.net/?retryWrites=true&w=majority`
5. Replace `<password>` with your actual password
6. **Save this** - you'll need it for Render

---

## Step 3: Deploy to Render

### 3.1 Sign Up / Login

1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up with GitHub (recommended) or email

### 3.2 Create Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### 3.3 Connect Repository

1. Click **"Connect account"** if needed (authorize GitHub)
2. Find and select your `pet-adoption-system` repository
3. Click **"Connect"**

### 3.4 Configure Service

Fill in the following:

- **Name:** `pet-adoption-system` (or any name)
- **Region:** Choose closest to you (e.g., `Oregon (US West)`)
- **Branch:** `main`
- **Root Directory:** (leave empty)
- **Environment:** `Python 3`
- **Build Command:** 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### 3.5 Add Environment Variable

1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. **Key:** `MONGO_URI`
4. **Value:** Your MongoDB Atlas connection string
   ```
   mongodb+srv://admin:YOUR_PASSWORD@pets-db.qxoxk2g.mongodb.net/?retryWrites=true&w=majority
   ```
   ⚠️ **Important:** Replace `YOUR_PASSWORD` with your actual MongoDB password
5. Click **"Add"**

### 3.6 Select Plan

- Choose **"Free"** for testing (spins down after inactivity)
- Or **"Starter"** ($7/month) for always-on production

### 3.7 Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for:
   - Build (installing dependencies)
   - Deployment (starting server)
3. Watch the logs in real-time

---

## Step 4: Verify Deployment

### 4.1 Check Deployment Status

- Green checkmark = Success ✅
- Red X = Failed ❌ (check logs)

### 4.2 Access Your App

Render provides a URL like:
```
https://pet-adoption-system.onrender.com
```

### 4.3 Test Your App

1. **Dashboard:** `https://your-app.onrender.com/dashboard`
2. **API Docs:** `https://your-app.onrender.com/docs`
3. **Animals API:** `https://your-app.onrender.com/api/animals`

---

## Step 5: Post-Deployment

### 5.1 Add Sample Data (Optional)

You can't run scripts directly on Render, but you can:
- Use the web interface to add data
- Or create a one-time script endpoint

### 5.2 Monitor Logs

- Go to Render dashboard
- Click on your service
- View **"Logs"** tab
- Check for errors or issues

### 5.3 Set Up Custom Domain (Optional)

1. Go to **"Settings"** → **"Custom Domains"**
2. Add your domain
3. Follow DNS configuration instructions

---

## 🔧 Troubleshooting

### Build Fails

**Error:** `ModuleNotFoundError`
- **Fix:** Check `requirements.txt` has all dependencies

**Error:** `Python version mismatch`
- **Fix:** Update `runtime.txt` or Render will auto-detect

### App Won't Start

**Error:** `Database connection failed`
- **Fix:** 
  - Check `MONGO_URI` environment variable
  - Verify MongoDB Atlas Network Access (0.0.0.0/0)
  - Check connection string format

**Error:** `Port already in use`
- **Fix:** Use `$PORT` in start command (already configured)

### Slow First Load

- **Normal:** Free tier spins down after 15 min inactivity
- **First request:** Takes 30-60 seconds to wake up
- **Solution:** Upgrade to Starter plan for always-on

---

## 📊 Your Deployment Status

✅ **Code:** Ready  
✅ **MongoDB Atlas:** Configured  
⏳ **GitHub:** Need to push  
⏳ **Render:** Need to deploy  

---

## 🚀 Quick Commands

```bash
# Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# Then deploy on Render (via web interface)
```

---

## 📝 Next Steps

1. **Push code to GitHub** (Step 1)
2. **Configure MongoDB Atlas** (Step 2)
3. **Deploy on Render** (Step 3)
4. **Test your live app** (Step 4)

**Need help with any step? Let me know!**


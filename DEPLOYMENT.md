# Deployment Guide - Pet Adoption System

## 🚀 Deployment Options

This guide covers deploying the Pet Adoption System to various platforms.

## Prerequisites

1. **MongoDB Atlas Account** (already set up)
   - Your `.env` file should have `MONGO_URI`
   - Ensure MongoDB Atlas allows connections from your deployment platform

2. **Git Repository** (recommended)
   - Push your code to GitHub/GitLab/Bitbucket

---

## Option 1: Railway (Recommended - Easiest) 🚂

Railway is excellent for FastAPI applications with automatic deployments.

### Steps:

1. **Sign up at [railway.app](https://railway.app)**

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo" (or upload code)

3. **Configure Environment Variables:**
   - Go to Project Settings → Variables
   - Add: `MONGO_URI` = your MongoDB connection string

4. **Deploy:**
   - Railway auto-detects Python projects
   - It will use `requirements.txt` automatically
   - Add build command: `pip install -r requirements.txt`
   - Add start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Get Your URL:**
   - Railway provides a URL like: `https://your-app.railway.app`

**Cost:** Free tier available, then $5/month

---

## Option 2: Render 🎨

Render offers free tier with automatic SSL.

### Steps:

1. **Sign up at [render.com](https://render.com)**

2. **Create New Web Service:**
   - Connect your GitHub repository
   - Select "Web Service"

3. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3
   - **Plan:** Free (or paid for better performance)

4. **Environment Variables:**
   - Add `MONGO_URI` in Environment section

5. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy automatically

**Cost:** Free tier available (spins down after inactivity), $7/month for always-on

---

## Option 3: Fly.io 🪰

Great for global deployment with edge locations.

### Steps:

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Initialize:**
   ```bash
   fly launch
   ```
   - Follow prompts
   - Don't deploy yet

4. **Set Environment Variables:**
   ```bash
   fly secrets set MONGO_URI="your-mongodb-uri"
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

**Cost:** Free tier available, pay-as-you-go

---

## Option 4: Heroku ☁️

Classic platform, now requires paid plans.

### Steps:

1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create App:**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set MONGO_URI="your-mongodb-uri"
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

**Cost:** $5/month minimum (no free tier)

---

## Option 5: Docker Deployment 🐳

Deploy using Docker to any platform (AWS, DigitalOcean, etc.)

### Steps:

1. **Build Docker Image:**
   ```bash
   docker build -t pet-adoption-system .
   ```

2. **Run Locally:**
   ```bash
   docker run -p 8000:8000 -e MONGO_URI="your-uri" pet-adoption-system
   ```

3. **Or use Docker Compose:**
   ```bash
   docker-compose up -d
   ```

4. **Push to Registry:**
   ```bash
   docker tag pet-adoption-system your-registry/pet-adoption-system
   docker push your-registry/pet-adoption-system
   ```

---

## Option 6: DigitalOcean App Platform 💧

Simple deployment with good performance.

### Steps:

1. **Sign up at [digitalocean.com](https://digitalocean.com)**

2. **Create App:**
   - Connect GitHub repository
   - Select "Web Service"

3. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** Add `MONGO_URI`

4. **Deploy:**
   - Click "Create Resources"

**Cost:** $5/month minimum

---

## 🔧 Production Configuration

### Update `main.py` for Production:

```python
if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=4,  # Adjust based on platform
        log_level="info"
    )
```

### Environment Variables Needed:

- `MONGO_URI` - MongoDB Atlas connection string (required)
- `PORT` - Server port (usually set by platform)

### MongoDB Atlas Configuration:

1. **Network Access:**
   - Go to MongoDB Atlas → Network Access
   - Add `0.0.0.0/0` to allow all IPs (or specific deployment IPs)

2. **Database User:**
   - Ensure your database user has read/write permissions

---

## 📝 Pre-Deployment Checklist

- [ ] All tests passing (`pytest tests/`)
- [ ] `.env` file has correct `MONGO_URI`
- [ ] MongoDB Atlas allows connections from deployment platform
- [ ] `requirements.txt` is up to date
- [ ] No hardcoded credentials in code
- [ ] Static files are properly configured
- [ ] Error handling is in place

---

## 🚨 Troubleshooting

### Common Issues:

1. **Database Connection Failed:**
   - Check MongoDB Atlas Network Access settings
   - Verify `MONGO_URI` is correct in environment variables
   - Check if MongoDB cluster is running (not paused)

2. **Port Issues:**
   - Most platforms set `PORT` environment variable
   - Use `os.getenv("PORT", 5001)` in code

3. **Static Files Not Loading:**
   - Ensure `frontend/static` directory is included in deployment
   - Check file paths in templates

4. **Build Failures:**
   - Check Python version compatibility
   - Verify all dependencies in `requirements.txt`

---

## 🎯 Recommended: Railway or Render

For easiest deployment, I recommend:
- **Railway** - Best for beginners, auto-detects everything
- **Render** - Free tier, good for testing

Both platforms:
- Auto-detect Python projects
- Handle SSL certificates automatically
- Provide easy environment variable management
- Support GitHub auto-deployments

---

## 📞 Need Help?

If you encounter issues during deployment:
1. Check platform logs
2. Verify environment variables
3. Test MongoDB connection
4. Review error messages

Good luck with your deployment! 🚀


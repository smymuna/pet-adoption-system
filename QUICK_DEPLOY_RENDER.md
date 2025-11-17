# Quick Deploy to Render - Step by Step

## 🚀 Fastest Way to Deploy Your Pet Adoption System

### Prerequisites
- GitHub account
- MongoDB Atlas connection string (you already have this)

---

## Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/pet-adoption-system.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)**
   - Sign up (free) or log in
   - Use GitHub to sign in (recommended)

2. **Create New Web Service:**
   - Click "New +" button (top right)
   - Select "Web Service"

3. **Connect Repository:**
   - Click "Connect account" if needed
   - Select your `pet-adoption-system` repository
   - Click "Connect"

4. **Configure Service:**
   - **Name:** `pet-adoption-system` (or any name you like)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variable:**
   - Scroll down to "Environment Variables"
   - Click "Add Environment Variable"
   - **Key:** `MONGO_URI`
   - **Value:** Your MongoDB Atlas connection string
     - Format: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`
   - Click "Add"

6. **Select Plan:**
   - Choose "Free" (for testing)
   - Or "Starter" ($7/month) for always-on

7. **Deploy:**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build and deployment

---

## Step 3: Configure MongoDB Atlas

1. **Allow Render IPs:**
   - Go to MongoDB Atlas → Network Access
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Or add Render's specific IP ranges
   - Click "Confirm"

2. **Verify Database User:**
   - Go to Database Access
   - Ensure your user has read/write permissions

---

## Step 4: Access Your App

Once deployment completes:
- Render provides a URL like: `https://pet-adoption-system.onrender.com`
- Click the URL to access your app
- First load might be slow (free tier spins down after inactivity)

---

## Step 5: Test Your Deployment

1. **Visit your app URL**
2. **Test the dashboard:** `https://your-app.onrender.com/dashboard`
3. **Test API:** `https://your-app.onrender.com/api/animals`
4. **Check API docs:** `https://your-app.onrender.com/docs`

---

## Troubleshooting

### App won't start:
- Check build logs in Render dashboard
- Verify `MONGO_URI` is set correctly
- Check that MongoDB Atlas allows connections

### Database connection fails:
- Verify MongoDB Atlas Network Access settings
- Check connection string format
- Ensure cluster is not paused

### Static files not loading:
- Verify `frontend/static` directory is in repository
- Check file paths in templates

---

## Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- **First request after spin-down takes 30-60 seconds**
- **512 MB RAM limit**
- **No custom domains on free tier**

For production, consider upgrading to Starter plan ($7/month).

---

## Next Steps

After deployment:
1. Test all features
2. Add sample data using `/utils/add_sample_data.py`
3. Share your app URL
4. Monitor logs in Render dashboard

**Your app is now live! 🎉**


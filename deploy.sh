#!/bin/bash
# Deployment Helper Script

echo "🚀 Pet Adoption System - Deployment Helper"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Check current status
echo "📋 Current Git Status:"
git status --short
echo ""

# Ask if user wants to commit
read -p "Do you want to commit all changes? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    git commit -m "Ready for deployment - $(date +%Y-%m-%d)"
    echo "✅ Changes committed"
    echo ""
fi

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo "🔗 GitHub Repository Setup:"
    echo "1. Go to https://github.com and create a new repository"
    echo "2. Name it: pet-adoption-system"
    echo "3. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL (or press Enter to skip): " repo_url
    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added"
        echo ""
    fi
fi

# Check if we can push
if git remote | grep -q "origin"; then
    read -p "Do you want to push to GitHub? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -M main
        git push -u origin main
        echo "✅ Pushed to GitHub"
        echo ""
    fi
fi

echo "=========================================="
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up / Login"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect your GitHub repository"
echo "5. Use these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "6. Add environment variable: MONGO_URI"
echo "7. Deploy!"
echo ""
echo "📖 See DEPLOY_MONGODB_ATLAS.md for detailed instructions"


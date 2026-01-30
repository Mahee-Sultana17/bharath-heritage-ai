# Render Deployment Guide for Bharath Heritage AI

## Changes Made for Production Deployment

### 1. **Backend Configuration (app.py)**
- ✅ Added environment variable support for `GROQ_API_KEY`
- ✅ Removed hardcoded API key
- ✅ Configured Flask to serve from correct template directory
- ✅ Added dynamic PORT configuration from environment
- ✅ Disabled debug mode in production
- ✅ Set host to `0.0.0.0` for external access

### 2. **Production Dependencies**
- ✅ Added `gunicorn` to requirements.txt for production WSGI server
- Gunicorn will handle concurrent requests better than Flask's development server

### 3. **Missing Templates**
- ✅ Created `home.html` (app.py was trying to render a non-existent template)

### 4. **Render Configuration**
- ✅ Created `render.yaml` with proper build and start commands
- Uses gunicorn with 4 workers for production workload
- Automatically installs dependencies from requirements.txt

### 5. **Environment Setup**
- ✅ Created `.env.example` for reference
- ✅ Created `.gitignore` to protect sensitive files

---

## Deployment Steps on Render

### Step 1: Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Connect to Render
1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Select the repository containing this code

### Step 3: Configure the Service
1. **Name**: `bharath-heritage-ai` (or your preferred name)
2. **Environment**: Select `Python 3`
3. **Region**: Choose closest to your target audience
4. **Branch**: `main` (or your default branch)
5. **Build Command**: Leave empty (render.yaml handles it)
6. **Start Command**: Leave empty (render.yaml handles it)

### Step 4: Set Environment Variables
1. In the Render dashboard, scroll to "Environment"
2. Add these variables:
   - **Key**: `GROQ_API_KEY` 
   - **Value**: Your actual Groq API key (from groq.com)

### Step 5: Deploy
- Click "Create Web Service"
- Render will automatically:
  - Clone your repository
  - Install dependencies
  - Build the application
  - Start the server

---

## Important Security Notes

⚠️ **NEVER commit `.env` files to version control**

- Your `.env` file is in `.gitignore` for safety
- Always use `.env.example` as a reference template
- Store sensitive keys (like `GROQ_API_KEY`) in Render's environment variables section

---

## Verification

Once deployed, test these endpoints:

- **Home Page**: `https://your-app-name.onrender.com/`
- **Places Category**: `https://your-app-name.onrender.com/category/places`
- **Arts Category**: `https://your-app-name.onrender.com/category/arts`
- **Festivals Category**: `https://your-app-name.onrender.com/category/festivals`

If you get 500 errors, check the Render logs for any missing environment variables.

---

## Troubleshooting

### Build Fails
- Check that all files are in the repository
- Verify requirements.txt has no syntax errors
- Ensure render.yaml is at the project root

### App Won't Start
- Verify `GROQ_API_KEY` is set in Render environment
- Check logs in Render dashboard
- Ensure Python version compatibility

### Template Not Found Errors
- The app.py now correctly points to the frontend folder
- Make sure `home.html`, `category.html`, and `detail.html` are in `googlehackathon/frontend/`

### Static Files Not Loading
- Verify `/static/images/` folder has required image files
- Check that Flask has correct template directory

---

## Local Testing Before Deployment

To test locally with production settings:

```bash
# Create .env file locally (not committed to git)
GROQ_API_KEY=your_test_key_here
FLASK_ENV=production
PORT=5000

# Run with gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 googlehackathon.backend.app:app
```

---

## File Changes Summary

| File | Change | Reason |
|------|--------|--------|
| `app.py` | Added environment variables, gunicorn support | Production deployment |
| `requirements.txt` | Added gunicorn | WSGI server for production |
| `home.html` | Created new file | Template was missing |
| `render.yaml` | Created new file | Render deployment config |
| `.env.example` | Created new file | Environment reference |
| `.gitignore` | Created new file | Protect secrets |

---

## Success Indicators

✅ App runs on `0.0.0.0:5000` 
✅ Environment variables configured
✅ All templates in correct location
✅ No hardcoded API keys in code
✅ Gunicorn ready for production
✅ Static files serve correctly

Your application is now ready for Render deployment!

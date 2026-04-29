# 🚀 Niyati Engine - Render Deployment Guide

## 📋 Prerequisites

1. **GitHub Account** - https://github.com
2. **Render Account** - https://render.com (sign up with GitHub)
3. **Git installed** on your computer

---

## 🛠️ Step-by-Step Deployment

### **Step 1: Prepare Your Project**

✅ Already done! The following files have been created:
- `render.yaml` - Render configuration
- `wsgi.py` - WSGI entry point
- `requirements.txt` updated with `gunicorn`
- `db.py` updated for production

---

### **Step 2: Push to GitHub**

Open terminal in your project folder and run:

```bash
# Initialize Git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Niyati Engine ready for Render"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/niyati-engine.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

### **Step 3: Deploy on Render**

1. **Go to Render:** https://dashboard.render.com

2. **Click:** "New +" → "Blueprint"

3. **Connect Repository:**
   - Select your `niyati-engine` repository
   - Click "Connect"

4. **Render will automatically:**
   - Read `render.yaml` configuration
   - Create PostgreSQL database
   - Deploy Flask backend
   - Set up environment variables

5. **Wait 5-10 minutes** for deployment to complete

---

### **Step 4: Initialize Database**

After deployment succeeds:

1. **Go to Render Dashboard**
2. **Click on your web service** (`niyati-engine`)
3. **Go to "Shell" tab**
4. **Run this command:**

```bash
python -c "from db import init_db; init_db()"
```

This creates all database tables.

---

### **Step 5: Access Your Live App**

Your app will be available at:
```
https://niyati-engine.onrender.com
```

But wait! You need to update the frontend to use this new URL.

---

## 🎨 Update Frontend URLs

### **Option 1: Hardcode Production URL**

Edit `frontend/script.js` and `frontend/auth.html`:

**Find:**
```javascript
http://localhost:5000
```

**Replace with:**
```javascript
https://niyati-engine.onrender.com
```

### **Option 2: Use Relative URLs (Better)**

Edit `frontend/script.js`:

**Find all instances of:**
```javascript
fetch(`http://localhost:5000/api/...`)
```

**Replace with:**
```javascript
fetch(`/api/...`)
```

Then serve the frontend from the same domain (see below).

---

## 🌐 Serve Frontend from Render

To serve the HTML files from Render:

### **Step 1: Move frontend files to root**

Create a `static` folder structure:

```
niyati-engine/
├── static/
│   ├── index.html
│   ├── auth.html
│   ├── style.css
│   └── script.js
├── api_server.py
├── db.py
└── ...
```

### **Step 2: Update api_server.py**

Add this after Flask app initialization:

```python
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'auth.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)
```

---

## 🔧 Environment Variables (Auto-Configured)

Render will automatically set these from `render.yaml`:

- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `FLASK_SECRET_KEY` - Auto-generated secret key
- `FLASK_DEBUG` - false (production mode)
- `FLASK_PORT` - 10000

---

## 📊 Render Free Tier Limits

- **Web Service:**
  - 512 MB RAM
  - 0.1 CPU
  - Spins down after 15 minutes of inactivity
  - First request after spin-down takes ~30 seconds

- **Database:**
  - 1 GB storage
  - Connects automatically
  - Backups included

---

## 🔍 Troubleshooting

### **Issue: "Application Error"**
- Check logs in Render Dashboard → Logs tab
- Common cause: Missing environment variables

### **Issue: Database Connection Failed**
- Ensure database is provisioned
- Check environment variables are set
- Run `init_db()` in Shell

### **Issue: Frontend can't connect to API**
- Update API URLs in `script.js`
- Check CORS settings in `api_server.py`
- Browser console will show errors

### **Issue: Models not loading**
- Ensure `.pkl` files are committed to Git
- Check file paths in `core_logic.py`

---

## 🎯 Production Checklist

- ✅ Update frontend API URLs
- ✅ Run database initialization
- ✅ Test all features (login, screening, history)
- ✅ Check mobile responsiveness
- ✅ Update team member details in footer
- ✅ Test profile edit functionality
- ✅ Verify screening history works

---

## 📱 Optional: Custom Domain

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. Go to Render Dashboard → Settings → Custom Domain
3. Add your domain
4. Update DNS records as instructed

---

## 🔄 Updating Your App

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Render will automatically redeploy!

---

## 💡 Tips

1. **Keep `.env` out of Git** - It's already in `.gitignore`
2. **Use Render logs** - Great for debugging
3. **Test locally first** - Before pushing to Git
4. **Monitor database usage** - Free tier has 1GB limit
5. **Wake up service** - Visit app daily to prevent spin-down

---

## 🆘 Need Help?

- **Render Docs:** https://render.com/docs
- **Flask Docs:** https://flask.palletsprojects.com
- **PostgreSQL Docs:** https://www.postgresql.org/docs

---

**Good luck with your deployment! 🚀**

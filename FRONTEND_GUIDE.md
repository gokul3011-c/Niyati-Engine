# 🎨 Niyati Engine - Beautiful Frontend Guide

## 🌟 What's New?

Your Niyati Engine now has a **stunning, modern frontend** with:

### ✨ Design Features
- **Crystal Glassmorphism Effect** - Frosted glass cards with beautiful transparency
- **Animated Background** - Floating crystal shapes with smooth animations
- **Gradient Colors** - Beautiful teal and purple gradients
- **Smooth Transitions** - Every interaction feels polished
- **Modern Typography** - Using Inter and Space Grotesk fonts
- **Responsive Layout** - Perfect on desktop, tablet, and mobile

### 🎯 UI Components
1. **Drag & Drop Upload Zone** - Intuitive file uploading
2. **Interactive Sliders** - Beautiful cutoff score control
3. **Stat Cards** - Animated counters for quick insights
4. **Candidate Cards** - Detailed profile with scores and skills
5. **Tab Navigation** - Smooth switching between accepted/rejected
6. **Analytics Dashboard** - Interactive charts (Pie & Bar)
7. **Loading Animation** - Crystal spinner during processing
8. **Toast Notifications** - Elegant success/error messages

## 🚀 How to Run

### Option 1: Quick Start (Recommended)
1. Double-click `start_server.bat`
2. Open `frontend/index.html` in your browser

### Option 2: Manual Start
```bash
# Terminal 1 - Start Backend
cd "Niyati Engine"
python api_server.py

# Terminal 2 - Open Frontend
# Just open frontend/index.html in your browser
```

## 📋 Workflow

1. **Upload Resumes**
   - Click the upload zone or drag & drop files
   - Supports: PDF, DOCX, JPG, PNG
   - Remove files by clicking the X icon

2. **Enter Job Description**
   - Type or paste the job requirements
   - Be detailed for better matching

3. **Set Cutoff Score**
   - Use the slider (0-100%)
   - Default is 70%

4. **Analyze**
   - Click "Analyze Resumes" button
   - Wait for AI processing

5. **View Results**
   - See statistics at the top
   - Browse accepted/rejected candidates
   - Check detailed skill analysis
   - View analytics charts

6. **Download**
   - Click "Download Results" to get CSV

## 🎨 Design Highlights

### Color Scheme
- **Primary**: #00ffd5 (Teal/Cyan)
- **Secondary**: #7c3aed (Purple)
- **Success**: #10b981 (Green)
- **Danger**: #ef4444 (Red)
- **Background**: Dark gradient

### Animations
- Floating crystals in background
- Pulse effect on logo
- Slide-in for file uploads
- Fade-in for results
- Smooth hover effects on cards
- Loading spinner

### Cards Design
- Frosted glass effect (backdrop-filter: blur)
- Subtle borders
- Gradient accents
- Shadow effects
- Hover transformations

## 🔌 Backend Connection

The frontend connects to the backend via REST API:

- **POST** `/api/analyze` - Analyze resumes
- **POST** `/api/download` - Download results

API runs on: `http://localhost:5000`

## 📊 Analytics Charts

Powered by Chart.js:
1. **Doughnut Chart** - Shows accepted vs rejected ratio
2. **Bar Chart** - Top 10 candidates' scores

## 🎯 Candidate Card Features

Each candidate card shows:
- Name and rank
- Predicted role
- Three key metrics:
  - Similarity %
  - Skill Match %
  - Final Score % (with progress bar)
- Matched skills (green tags)
- Missing skills (red tags)
- Top match badge for #1 candidate

## 💡 Tips for Best Experience

1. Use Chrome or Edge browser for best performance
2. Keep backend server running while using frontend
3. Upload multiple resumes for better comparison
4. Detailed job descriptions give better results
5. Adjust cutoff based on your needs

## 🐛 Troubleshooting

**Frontend not loading?**
- Check if index.html exists in frontend folder
- Try opening with Live Server

**API not responding?**
- Make sure api_server.py is running
- Check console for errors
- Verify port 5000 is not in use

**Charts not showing?**
- Check internet connection (Chart.js loads from CDN)
- Wait for results to load completely

## 🎉 Enjoy Your New Interface!

Your Niyati Engine now has a professional, modern interface that makes resume screening a beautiful experience!

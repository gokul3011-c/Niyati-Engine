# Niyati Engine - AI Resume Screening System

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend API Server
```bash
python api_server.py
```
The backend will run on `http://localhost:5000`

### 3. Open the Frontend
Simply open `frontend/index.html` in your web browser, or:
- Use Live Server extension in VS Code
- Or run a simple HTTP server:
```bash
cd frontend
python -m http.server 8000
```
Then visit `http://localhost:8000`

## ✨ Features

- 🎨 **Crystal Glassmorphism UI** - Modern, attractive design
- 📤 **Drag & Drop** - Easy resume upload (PDF, DOCX, Images)
- 📊 **Real-time Analytics** - Beautiful charts and visualizations
- 🏆 **Smart Ranking** - AI-powered candidate ranking
- 📥 **Export Results** - Download results as CSV
- 🎯 **Skill Matching** - Detailed skill gap analysis
- 📱 **Responsive Design** - Works on all devices

## 🎯 How to Use

1. Upload resumes (supports PDF, DOCX, JPG, PNG)
2. Enter the job description
3. Adjust the cutoff score slider
4. Click "Analyze Resumes"
5. View detailed results with analytics

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Backend**: Flask, Python
- **AI/ML**: Scikit-learn, PDFPlumber, PyTesseract
- **Design**: Glassmorphism, CSS Animations

## 📝 Notes

- Make sure Tesseract OCR is installed for image-based PDFs
- The backend must be running before using the frontend
- Supports multiple file uploads simultaneously

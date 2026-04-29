# 🧠 Niyati Engine
### AI-Powered Resume Screening System

**Niyati Engine** is a comprehensive, production-ready web application that automates candidate evaluation by intelligently analyzing resumes against job descriptions. Built with modern web technologies, it helps recruiters and HR professionals identify the best candidates efficiently using Natural Language Processing (NLP), Machine Learning, and a beautiful responsive user interface.

---

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [How It Works](#-how-it-works)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [User Guide](#-user-guide)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)
- [Scoring System](#-scoring-system)
- [Use Cases](#-use-cases)
- [Future Enhancements](#-future-enhancements)
- [Troubleshooting](#-troubleshooting)
- [Author](#-author)

---

## ✨ Features

### 🎯 Core Features
- **Multi-format Resume Upload**: Support for PDF, DOCX, JPG, JPEG, PNG files
- **Drag & Drop Interface**: Intuitive file upload with drag-and-drop support
- **AI-Powered Analysis**: Advanced NLP and ML-based resume parsing
- **TF-IDF Similarity Scoring**: Intelligent text similarity calculation
- **Skill Matching System**: Automatic skill extraction and comparison
- **Role Prediction**: ML model predicts candidate's suitable role
- **Experience Scoring**: Calculates years of experience and relevance
- **Weighted Final Score**: Combines multiple metrics for accurate ranking
- **Cutoff-based Filtering**: Customizable threshold for candidate selection
- **Accepted/Rejected Classification**: Clear candidate categorization

### 👤 User Management
- **User Authentication**: Secure login and signup system
- **Profile Management**: Editable user profile with name, company, and email
- **Session History**: Track all previous screening sessions
- **Data Persistence**: User data stored securely in PostgreSQL database

### 📊 Analytics & Reporting
- **Interactive Dashboard**: Real-time analytics with charts
- **Pie Charts**: Visual representation of accepted vs rejected candidates
- **Bar Charts**: Top candidates score comparison
- **CSV Export**: Download screening results for offline analysis
- **Screening History**: View and revisit past analyses

### 📱 User Interface
- **Modern Design**: Glass-morphism UI with crystal animations
- **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- **Touch-Friendly**: Mobile-optimized touch targets and interactions
- **Dark Theme**: Eye-friendly dark color scheme
- **Smooth Animations**: Engaging transitions and loading states
- **Notification System**: Real-time success/error/warning notifications

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  FRONTEND LAYER                      │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ HTML/CSS  │  │  JavaScript│  │   Chart.js      │ │
│  │ (Responsive│  │  (ES6+)   │  │   (Analytics)   │ │
│  │  Design)  │  │           │  │                 │ │
│  └───────────┘  └──────────┘  └──────────────────┘ │
└──────────────────────┬──────────────────────────────┘
                       │ REST API (HTTP/JSON)
┌──────────────────────▼──────────────────────────────┐
│                  BACKEND LAYER                       │
│  ┌──────────────────────────────────────────────┐   │
│  │         Flask Server (api_server.py)         │   │
│  │  ┌────────────┐  ┌──────────────────────┐   │   │
│  │  │ Auth APIs  │  │  Analysis APIs       │   │   │
│  │  │ Login/     │  │  - Upload & Analyze  │   │   │
│  │  │ Signup     │  │  - Get History       │   │   │
│  │  │ Profile    │  │  - Download Results  │   │   │
│  │  │ Management │  │  - Delete Sessions   │   │   │
│  │  └────────────┘  └──────────────────────┘   │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│               BUSINESS LOGIC LAYER                   │
│  ┌──────────────────────────────────────────────┐   │
│  │         core_logic.py                        │   │
│  │  • Text Extraction (PDF/DOCX/OCR)           │   │
│  │  • Text Preprocessing & Cleaning            │   │
│  │  • TF-IDF Vectorization                     │   │
│  │  • Similarity Calculation                   │   │
│  │  • Skill Matching                           │   │
│  │  • Experience Scoring                       │   │
│  │  • Role Prediction (ML Model)               │   │
│  │  • Final Score Calculation                  │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  DATA LAYER                          │
│  ┌────────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ PostgreSQL │  │ ML Model │  │  Vectorizer  │   │
│  │ Database   │  │  (.pkl)  │  │   (.pkl)     │   │
│  │            │  │          │  │              │   │
│  │ • Users    │  │ Role     │  │ TF-IDF       │   │
│  │ • Sessions │  │ Predictor│  │ Vectorizer   │   │
│  │ • Candidates│ │          │  │              │   │
│  └────────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with CSS Grid, Flexbox, animations
- **JavaScript (ES6+)**: Interactive functionality, async/await
- **Chart.js**: Data visualization and analytics
- **Font Awesome 6.4**: Icon library
- **Google Fonts**: Inter & Space Grotesk typography

### Backend
- **Python 3.13**: Core programming language
- **Flask**: Lightweight WSGI web framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **bcrypt**: Password hashing and security
- **psycopg2**: PostgreSQL database adapter
- **python-dotenv**: Environment variable management

### Machine Learning & NLP
- **scikit-learn**: ML algorithms and TF-IDF vectorization
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **pickle**: Model serialization

### Document Processing
- **pdfplumber**: PDF text extraction
- **python-docx**: DOCX file parsing
- **pytesseract**: OCR for image-based resumes
- **Pillow**: Image processing

### Database
- **PostgreSQL**: Relational database management
- **SQL**: Database queries and schema management

---

## 🔄 How It Works

### User Flow
1. **User Registration/Login** → Create account or login
2. **Upload Resumes** → Drag & drop or browse files
3. **Enter Job Description** → Paste job requirements
4. **Set Cutoff Score** → Adjust minimum threshold (0-100%)
5. **Analyze** → Click to start AI processing
6. **View Results** → See ranked candidates with scores
7. **Analytics** → View charts and insights
8. **Export** → Download results as CSV

### Processing Pipeline
```
Upload Files
    ↓
Text Extraction (PDF/DOCX/OCR)
    ↓
Text Preprocessing (Clean, Tokenize)
    ↓
Role Prediction (ML Model)
    ↓
TF-IDF Vectorization
    ↓
Similarity Calculation (Resume vs JD)
    ↓
Skill Matching (Extracted vs Required)
    ↓
Experience Scoring (Years vs Required)
    ↓
Final Score Calculation (Weighted Sum)
    ↓
Ranking (Sort by Score)
    ↓
Filtering (Apply Cutoff)
    ↓
Display Results + Analytics
    ↓
Save to Database
```

---

## 📦 Installation & Setup

### Prerequisites
- **Python 3.13** or higher
- **PostgreSQL 12+** installed and running
- **Git** (optional, for version control)

### Step 1: Clone or Download
```bash
# If using Git
git clone <your-repo-link>
cd "Niyati Engine new"

# Or extract the downloaded folder
cd "Niyati Engine new"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
Create a `.env` file in the root directory:
```env
# Database Configuration
DB_NAME=Niyati_Engine
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here
```

### Step 4: Setup Database
```bash
# Create database in PostgreSQL
psql -U postgres
CREATE DATABASE "Niyati_Engine";
\q

# Run schema
psql -U postgres -d Niyati_Engine -f database_schema.sql
```

Or use the database schema file manually in pgAdmin/your PostgreSQL client.

### Step 5: Add Company Column
```bash
python add_company_column.py
```

---

## 🚀 Running the Application

### Option 1: Quick Start (Windows)
```bash
# Double-click or run:
start_server.bat
```

### Option 2: Manual Start
```bash
# Start the backend server
python api_server.py
```

The server will start at: **http://localhost:5000**

### Option 3: Open Frontend
```bash
# Open launch.html in your browser
start launch.html

# Or navigate to:
frontend/index.html
```

### Access Points
- **Launch Page**: `launch.html`
- **Frontend App**: `frontend/index.html`
- **Backend API**: `http://localhost:5000`
- **API Docs**: See [API Documentation](#api-documentation)

---

## 📖 User Guide

### Getting Started

#### 1. Create an Account
1. Open the application
2. Click "Sign Up" tab
3. Fill in:
   - Company Name (optional)
   - Username (required)
   - Email (optional)
   - Password (required)
4. Click "Sign Up"
5. Login with your credentials

#### 2. Upload Resumes
1. Click the upload zone or drag & drop files
2. Supported formats: PDF, DOCX, JPG, JPEG, PNG
3. Multiple files supported
4. Remove files by clicking the ✕ icon

#### 3. Enter Job Description
1. Paste the complete job description in the textarea
2. Include required skills, experience, qualifications
3. Be specific for better matching

#### 4. Set Cutoff Score
1. Use the slider to set minimum threshold (0-100%)
2. Default: 70%
3. Candidates below cutoff will be marked as "Rejected"

#### 5. Analyze Resumes
1. Click "Analyze Resumes" button
2. Wait for processing (loading animation appears)
3. Results will display automatically

#### 6. View Results
- **Stats Cards**: Total, Accepted, Rejected counts
- **Accepted Tab**: Candidates above cutoff
- **Rejected Tab**: Candidates below cutoff
- **Candidate Cards**: Detailed breakdown with:
  - Final Score (large display)
  - Similarity, Experience, Skill Match scores
  - Matched Skills (green)
  - Missing Skills (red)
  - Predicted Role

#### 7. Analytics Dashboard
- **Pie Chart**: Accepted vs Rejected distribution
- **Bar Chart**: Top 10 candidates score comparison
- Color-coded: Green (accepted), Red (rejected)

#### 8. Download Results
1. Click "Download Results" button
2. CSV file downloads automatically
3. Contains all candidate data and scores

#### 9. Settings Panel
Click the ⚙️ icon to access:
- **Screening History**: View past analyses
- **View Details**: Click any history item to reload results
- **Delete Screenings**: Select and remove old sessions
- **Logout**: Sign out of your account

#### 10. Profile Management
1. Click your profile icon (avatar)
2. View your profile information:
   - Name
   - Company
   - Email
3. Click ✏️ (edit icon) to modify:
   - Update any field
   - Click "Save Changes"
   - Cancel to discard changes

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication Endpoints

#### POST /api/signup
Register a new user
```json
Request:
{
  "company": "Tech Corp",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword"
}

Response (201):
{
  "message": "Signup successful",
  "user_id": 1,
  "username": "johndoe",
  "company": "Tech Corp"
}
```

#### POST /api/login
Authenticate user
```json
Request:
{
  "username": "johndoe",
  "password": "securepassword"
}

Response (200):
{
  "message": "Login successful",
  "user_id": 1,
  "username": "johndoe",
  "company": "Tech Corp",
  "email": "john@example.com"
}
```

### User Profile Endpoints

#### GET /api/user/:user_id/profile
Get user profile information
```
Response (200):
{
  "user_id": 1,
  "company": "Tech Corp",
  "username": "johndoe",
  "email": "john@example.com",
  "member_since": "2024-01-15T10:30:00",
  "last_login": "2024-01-20T15:45:00",
  "stats": {
    "total_sessions": 5,
    "total_candidates_analyzed": 50,
    "total_accepted": 30,
    "total_rejected": 20,
    "average_score": 72.5
  }
}
```

#### PUT /api/user/:user_id/profile
Update user profile
```json
Request:
{
  "username": "newname",
  "company": "New Company",
  "email": "new@email.com"
}

Response (200):
{
  "message": "Profile updated successfully",
  "user_id": 1,
  "username": "newname",
  "company": "New Company",
  "email": "new@email.com"
}
```

### Analysis Endpoints

#### POST /api/analyze
Analyze resumes against job description
```
Content-Type: multipart/form-data

Form Data:
- user_id: 1
- job_description: "We are looking for..."
- cutoff: 70
- resumes: [file1.pdf, file2.docx, ...]

Response (200):
{
  "total": 10,
  "accepted": 6,
  "rejected": 4,
  "accepted_candidates": [...],
  "rejected_candidates": [...],
  "all_candidates": [...]
}
```

#### GET /api/user/:user_id/history
Get user's screening history
```
Response (200):
{
  "sessions": [
    {
      "session_id": 1,
      "job_description": "...",
      "cutoff_score": 70,
      "total_candidates": 10,
      "accepted_count": 6,
      "rejected_count": 4,
      "created_at": "2024-01-20T15:45:00"
    }
  ]
}
```

#### GET /api/session/:session_id
Get detailed session results
```
Response (200):
{
  "session_id": 1,
  "total_candidates": 10,
  "accepted_count": 6,
  "rejected_count": 4,
  "candidates": [...]
}
```

#### POST /api/download
Download results as CSV
```json
Request:
{
  "results": [...]
}

Response (200):
CSV file download
```

### Management Endpoints

#### POST /api/screenings/delete
Delete screening sessions
```json
Request:
{
  "user_id": 1,
  "session_ids": [1, 2, 3]
}

Response (200):
{
  "message": "3 screenings deleted successfully"
}
```

### Error Responses
```json
400 Bad Request:
{
  "error": "Descriptive error message"
}

401 Unauthorized:
{
  "error": "User not logged in"
}

404 Not Found:
{
  "error": "Resource not found"
}

409 Conflict:
{
  "error": "Username already exists"
}

500 Internal Server Error:
{
  "error": "Server error details"
}
```

---

## 🗄️ Database Schema

### Tables

#### users
Stores user authentication and profile data
```sql
- id (SERIAL, PRIMARY KEY)
- username (VARCHAR(100), UNIQUE, NOT NULL)
- password (VARCHAR(255), NOT NULL) - bcrypt hashed
- email (VARCHAR(150), UNIQUE)
- company (VARCHAR(200))
- created_at (TIMESTAMP)
- last_login (TIMESTAMP)
- is_active (BOOLEAN, DEFAULT TRUE)
```

#### analysis_sessions
Tracks each resume analysis session
```sql
- id (SERIAL, PRIMARY KEY)
- user_id (INTEGER, FK to users)
- job_description (TEXT)
- cutoff_score (DECIMAL)
- total_candidates (INTEGER)
- accepted_count (INTEGER)
- rejected_count (INTEGER)
- created_at (TIMESTAMP)
```

#### candidates
Stores candidate resume analysis results
```sql
- id (SERIAL, PRIMARY KEY)
- user_id (INTEGER, FK to users)
- name (VARCHAR(200))
- role (VARCHAR(100))
- similarity (DECIMAL)
- skill (DECIMAL)
- experience (DECIMAL)
- final_score (DECIMAL)
- matched_skills (TEXT[])
- missing_skills (TEXT[])
- job_description (TEXT)
- cutoff_score (DECIMAL)
- status (VARCHAR - 'accepted'/'rejected')
- created_at (TIMESTAMP)
```

### Indexes
- `idx_candidates_user_id`: Fast user lookups
- `idx_candidates_final_score`: Score-based sorting
- `idx_candidates_status`: Status filtering
- `idx_analysis_sessions_user_id`: Session queries
- `idx_analysis_sessions_created_at`: Time-based queries

---

## 📁 Project Structure

```
Niyati Engine new/
│
├── 📄 README.md                    # Project documentation
├── 📄 .env                         # Environment variables (DO NOT COMMIT)
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
│
├── 🔧 api_server.py                # Main Flask backend server (528 lines)
├── 🧠 core_logic.py                # AI/ML processing logic (20.2KB)
├── 💾 db.py                        # Database connection handler
├── 📊 database_schema.sql          # PostgreSQL schema
│
├── 📦 requirements.txt             # Python dependencies
├── 🚀 start_server.bat             # Windows quick start script
├── 🌐 launch.html                  # Application launcher page
│
├── 🤖 model.pkl                    # Trained ML role prediction model
├── 📝 vectorizer.pkl               # TF-IDF vectorizer
├── 🏷️ label_encoder.pkl            # Label encoder for roles
│
└── 🎨 frontend/                    # Frontend web application
    ├── 📄 index.html               # Main application page (276 lines)
    ├── 🔐 auth.html                # Login/Signup page (429 lines)
    ├── 📜 script.js                # Frontend JavaScript (900+ lines)
    ├── 🎨 style.css                # Styles with responsive design (1800+ lines)
    └── 📖 README.md                # Frontend documentation
```

---

## 📊 Scoring System

### Final Score Calculation
```
Final Score = (Similarity Score) + (Skill Match Score) + (Experience Score)
```

### Component Breakdown

#### 1. Similarity Score (0-100%)
- Based on TF-IDF cosine similarity
- Compares resume text with job description
- Measures overall content relevance

#### 2. Skill Match Score (0-100%)
- Extracts skills from resume and JD
- Calculates percentage of matched skills
- Formula: (Matched Skills / Total Required Skills) × 100

#### 3. Experience Score (0-100%)
- Extracts years of experience from resume
- Compares with JD requirements
- Returns 100% if experience meets/exceeds requirement
- Returns 0% if no experience mentioned
- Proportional scoring for partial matches

### Example
```
Candidate: John Doe
- Similarity: 75%
- Skill Match: 80% (8/10 skills matched)
- Experience: 100% (5 years vs 3 required)

Final Score = 75 + 80 + 100 = 255 (normalized to percentage)
```

---

## 💡 Use Cases

### Primary Use Cases
- **Campus Recruitment**: Screen hundreds of resumes efficiently
- **Corporate Hiring**: Automate initial resume screening
- **HR Departments**: Reduce manual screening workload
- **Recruitment Agencies**: Process client requirements faster

### Advanced Use Cases
- **Skill Gap Analysis**: Identify missing skills in candidate pool
- **Market Research**: Analyze available talent for specific roles
- **Benchmarking**: Compare candidate quality across positions
- **Reporting**: Generate hiring metrics and insights

---

## 🚀 Future Enhancements

### Planned Features
- [ ] **Admin Dashboard**: Centralized user and analytics management
- [ ] **AI Feedback**: Automated suggestions for job descriptions
- [ ] **Email Notifications**: Alert candidates of their status
- [ ] **Advanced Filters**: Filter by skills, experience, score range
- [ ] **Bulk Upload**: Upload JD templates and batch process
- [ ] **API Integration**: LinkedIn, Indeed job posting integration
- [ ] **Multi-language Support**: Resume analysis in multiple languages
- [ ] **Video Interviews**: Integrated video screening
- [ ] **Mobile App**: Native iOS/Android application
- [ ] **Cloud Deployment**: AWS/Azure deployment guides

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
Error: Connection refused
Solution:
- Ensure PostgreSQL is running
- Check credentials in .env file
- Verify database exists: CREATE DATABASE "Niyati_Engine";
```

#### 2. Port Already in Use
```
Error: Address already in use
Solution:
- Kill existing process: netstat -ano | findstr :5000
- Or change port in api_server.py
```

#### 3. Module Not Found
```
Error: No module named 'xyz'
Solution:
- Run: pip install -r requirements.txt
- Ensure correct Python version (3.13+)
```

#### 4. File Upload Fails
```
Error: Unsupported file format
Solution:
- Check file is PDF, DOCX, JPG, JPEG, or PNG
- Ensure file is not corrupted
- Check file size limits
```

#### 5. Tesseract OCR Error
```
Error: tesseract not found
Solution:
- Install Tesseract: https://github.com/tesseract-ocr/tesseract
- Add to system PATH
- Restart server
```

#### 6. CORS Issues
```
Error: CORS policy blocked
Solution:
- Ensure Flask-CORS is installed
- Check frontend API URL matches backend
- Verify server is running on port 5000
```

### Debug Mode
To enable debug mode, modify `api_server.py`:
```python
app.run(debug=True, port=5000)
```

### Logs
Check terminal output for detailed error messages and processing logs.

---

## 📈 Performance

### Optimization Features
- **Connection Pooling**: Efficient database connections
- **Lazy Loading**: Charts render only when needed
- **Caching**: LocalStorage for user session data
- **Async Processing**: Non-blocking UI during analysis
- **Responsive Images**: Optimized for all screen sizes

### Recommended Specs
- **Minimum**: 4GB RAM, Dual-core CPU
- **Recommended**: 8GB RAM, Quad-core CPU
- **Database**: PostgreSQL 12+ with 2GB+ storage
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+

---

## 🔐 Security

### Security Measures
- **Password Hashing**: bcrypt with salt rounds
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Input sanitization
- **CORS Configuration**: Controlled API access
- **Environment Variables**: Secure credential storage
- **Session Management**: LocalStorage with validation

### Best Practices
- Never commit `.env` file
- Use strong passwords
- Regular database backups
- Keep dependencies updated
- Monitor server logs

---

## 📝 License

This project is created for educational and demonstration purposes.

---

## 👨‍💻 Author

**Gokul**  
Engineering Student

---

## 🙏 Acknowledgments

- Font Awesome for icons
- Chart.js for analytics visualization
- Google Fonts for typography
- Open-source ML libraries
- PostgreSQL community

---

## 📞 Support

For issues, questions, or contributions:
- Check the [Troubleshooting](#-troubleshooting) section
- Review API documentation
- Verify database setup
- Check server logs

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star! ⭐**

Made with ❤️

</div>

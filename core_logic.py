import pdfplumber
from PIL import Image
from docx import Document
import os
import platform

# Try to import pytesseract, but don't fail if it's not available
try:
    import pytesseract
    
    # Set Tesseract path based on operating system
    try:
        if platform.system() == 'Windows':
            # Windows path
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        else:
            # Linux/Mac (Render uses Linux)
            pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
    except Exception:
        pass  # Tesseract will use default path
        
    TESSERACT_AVAILABLE = True
except Exception:
    TESSERACT_AVAILABLE = False
    print("⚠️  Tesseract OCR not available. Image-based PDFs will be skipped.")

import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
le = joblib.load("label_encoder.pkl")

import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
le = joblib.load("label_encoder.pkl")

#list/dictionaries

SKILLS = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "ruby",

    # Web Development
    "html", "css", "react", "angular", "node", "bootstrap", "vue",

    # Backend / Frameworks
    "django", "flask", "spring", "spring boot", "express",

    # Data Science / AI
    "machine learning", "deep learning", "natural language processing",
    "data science", "data analysis", "data visualization",

    # Libraries
    "pandas", "numpy", "matplotlib", "seaborn",
    "tensorflow", "pytorch", "scikit learn",

    # Databases
    "sql", "mongodb", "oracle", "redis",

    # DevOps / Cloud
    "docker", "kubernetes", "aws", "azure", "gcp",

    # Big Data
    "hadoop", "spark", "kafka",

    # Testing / QA
    "selenium", "automation testing", "unit testing",

    # Security
    "network security", "encryption", "cyber security",

    # Tools
    "git", "github", "ci cd",
    "api", "apis", "restful api",
    "backend", "frontend", "full stack",
    "developer", "web development",
    "projects",
    "objective",
    "technical skills", "tech stack",
    "web development", "web applications",
    "backend", "backend development",
    "system design", "software development",
    "api", "apis", "rest api",
    "full stack",
    # ---------------- MEDICAL ----------------
    "patient care", "clinical research", "diagnosis", "medical coding",
    "hospital management", "nursing", "healthcare", "treatment planning",

         # ---------------- PHARMACY ----------------
      "pharmacology", "drug dispensing", "medication management",
        "clinical trials", "pharmaceutical analysis",

     # ---------------- CIVIL ----------------
           "autocad", "construction", "site engineering",
        "structural design", "surveying", "civil engineering",
      "project planning", "quantity surveying",

# ---------------- ECE ----------------
"embedded systems", "vlsi", "signal processing",
"microcontrollers", "pcb design", "electronics",

# ---------------- EEE ----------------
"power systems", "electrical circuits",
"transformers", "control systems", "electrical engineering",

# ---------------- MECHANICAL ----------------
"solidworks", "thermodynamics", "manufacturing",
"ansys", "cad", "mechanical design", "hvac",

# ---------------- SOCIAL MEDIA / MARKETING ----------------
"seo", "digital marketing", "content creation",
"social media marketing", "google analytics",
"branding", "campaign management", "advertising",

"teaching", "classroom management", "lesson planning",
"curriculum development", "student assessment",
"education", "training", "mentoring",
"blackboard", "smart class", "e learning",
"online teaching", "tutoring", "academic",
"subject knowledge", "pedagogy",
"communication skills", "presentation skills"
]

SYNONYMS = {
    # AI / Data
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",

    "data analytics": "data analysis",
    "data analyst": "data analysis",
    "data scientist": "data science",

    # Programming
    "python3": "python",

    "js": "javascript",
    "nodejs": "node",
    "node.js": "node",

    "reactjs": "react",
    "angularjs": "angular",

    # Databases
    "sql server": "sql",
    "mysql": "sql",
    "postgresql": "sql",
    "sqlite": "sql",

    # Cloud
    "amazon web services": "aws",
    "aws cloud": "aws",
    "azure cloud": "azure",
    "google cloud": "gcp",

    # DevOps
    "docker container": "docker",
    "k8s": "kubernetes",

    # Other
    "frontend": "frontend development",
    "backend": "backend development",

    # ---------------- AI / DATA ----------------
"ml engineer": "machine learning",
"ai engineer": "artificial intelligence",
"data analytics": "data analysis",
"data analyst": "data analysis",
"data scientist": "data science",

# ---------------- PROGRAMMING ----------------
"py": "python",
"python3": "python",
"js": "javascript",
"ts": "typescript",
"nodejs": "node",
"node.js": "node",
"reactjs": "react",
"angularjs": "angular",

# ---------------- DATABASE ----------------
"sql server": "sql",
"mysql": "sql",
"postgresql": "sql",
"sqlite": "sql",
"nosql": "mongodb",

# ---------------- CLOUD ----------------
"amazon web services": "aws",
"aws cloud": "aws",
"azure cloud": "azure",
"google cloud": "gcp",
"gcp cloud": "gcp",

# ---------------- DEVOPS ----------------
"docker container": "docker",
"k8s": "kubernetes",
"ci/cd": "ci cd",

# ---------------- MEDICAL ----------------
"bp": "blood pressure",
"ecg": "electrocardiogram",
"ehr": "electronic health record",
"emr": "electronic medical record",

# ---------------- PHARMACY ----------------
"rx": "prescription",
"meds": "medication",

# ---------------- CIVIL ----------------
"cad": "computer aided design",
"site work": "construction",
"structural analysis": "structural design",

# ---------------- ECE ----------------
"pcb": "printed circuit board",
"vlsi design": "vlsi",

# ---------------- EEE ----------------
"power grid": "power systems",

# ---------------- MECHANICAL ----------------
"solid works": "solidworks",
"thermo": "thermodynamics",

# ---------------- MARKETING ----------------
"smm": "social media marketing",
"seo optimization": "seo",
"digital ads": "advertising",

# ---------------- GENERAL ----------------
"frontend": "frontend development",
"backend": "backend development",
"fullstack": "full stack",

"teacher": "teaching",
"tutor": "teaching",
"lecturer": "teaching",
"professor": "teaching",
"faculty": "teaching",

"online tutor": "online teaching",
"virtual teaching": "online teaching",

"classroom teaching": "teaching",
"academic teaching": "teaching"

}

ROLE_RULES = {

    # FRONTEND
    "Frontend Developer": ["html", "css", "javascript", "react", "angular", "vue"],

    # BACKEND
    "Backend Developer": ["node", "django", "flask", "spring", "sql", "api"],

    # FULL STACK
    "Full Stack Developer": ["html", "css", "javascript", "node", "react"],

    # DATA
    "Data Scientist": ["machine learning", "pandas", "numpy", "tensorflow", "python"],
    "Data Analyst": ["excel", "sql", "power bi", "tableau"],
    "ML Engineer": ["machine learning", "tensorflow", "pytorch", "deep learning"],

    # DEVOPS
    "DevOps Engineer": ["docker", "kubernetes", "aws", "ci", "cd"],
    "Cloud Engineer": ["aws", "azure", "gcp"],

    # DATABASE
    "Database Engineer": ["sql", "mysql", "postgresql", "mongodb"],
    "Data Engineer": ["spark", "hadoop", "etl", "sql"],

    # MOBILE
    "Android Developer": ["java", "kotlin", "android"],
    "iOS Developer": ["swift", "ios"],

    # TESTING
    "QA Engineer": ["testing", "manual testing"],
    "QA Automation Engineer": ["selenium", "automation", "testing"],

    # SECURITY
    "Security Engineer": ["cyber security", "penetration testing", "network security"],

    # AI
    "AI Engineer": ["artificial intelligence", "deep learning", "nlp"],

    # SOFTWARE
    "Software Engineer": ["c", "c++", "java", "python"],

    # NETWORK
    "Network Engineer": ["networking", "tcp", "ip"],

    # SYSTEM
    "System Administrator": ["linux", "server", "system admin"],

    # BLOCKCHAIN
    "Blockchain Developer": ["blockchain", "ethereum", "solidity"],

    # GAME
    "Game Developer": ["unity", "unreal", "c#"],

    # UI/UX
    "UI/UX Designer": ["figma", "ui", "ux"],

    # EMBEDDED
    "Embedded Engineer": ["embedded", "microcontroller", "iot"],

    # BUSINESS
    "Business Analyst": ["analysis", "requirement gathering"],

    # PROJECT
    "Project Manager": ["project management", "agile", "scrum"],

    # ---------------- MEDICAL ----------------
"Doctor": ["patient", "diagnosis", "clinical", "hospital", "treatment"],
"Nurse": ["nursing", "patient care", "healthcare"],
"Medical Lab Technician": ["lab", "testing", "blood", "sample"],

# ---------------- PHARMACY ----------------
"Pharmacist": ["drug", "pharmacy", "medication", "prescription"],
"Clinical Pharmacist": ["clinical trials", "medication", "drug"],

# ---------------- CIVIL ----------------
"Civil Engineer": ["construction", "autocad", "site", "structural"],
"Site Engineer": ["site", "construction", "project"],
"Structural Engineer": ["structural", "design", "analysis"],

# ---------------- ECE ----------------
"ECE Engineer": ["embedded", "vlsi", "signal", "electronics"],
"Embedded Engineer": ["embedded", "microcontroller", "iot"],
"VLSI Engineer": ["vlsi", "chip", "design"],

# ---------------- EEE ----------------
"EEE Engineer": ["power", "electrical", "circuit", "transformer"],
"Electrical Engineer": ["electrical", "power systems"],
"Power Systems Engineer": ["power", "grid", "electricity"],

# ---------------- MECHANICAL ----------------
"Mechanical Engineer": ["cad", "thermodynamics", "manufacturing", "solidworks"],
"Design Engineer": ["design", "cad", "solidworks"],
"Production Engineer": ["manufacturing", "production"],

# ---------------- MARKETING ----------------
"Digital Marketer": ["seo", "marketing", "content", "social media"],
"Social Media Manager": ["social media", "content", "campaign"],
"SEO Specialist": ["seo", "optimization"],
"Content Creator": ["content", "writing", "media"],

# ---------------- TEACHING ----------------
"Teacher": ["teaching", "classroom", "lesson", "student"],
"Lecturer": ["teaching", "academic", "subject", "lecture"],
"Professor": ["research", "teaching", "academic"],
"Tutor": ["teaching", "tutoring", "student"],
"Trainer": ["training", "mentoring", "session"]
    
}


CATEGORY_MAP = {
    "Java Developer": "Backend / Web Developer",
    "Web Designing": "Frontend Developer",
    "DotNet Developer": "Backend Developer",
    "Python Developer": "Backend / Data Developer",
    "Data Science": "Data Scientist",
    "Hadoop": "Big Data Engineer",
    "DevOps Engineer": "DevOps Engineer",
    "Database": "Database Engineer",
    "Testing": "QA / Testing Engineer",
    "Automation Testing": "QA Automation Engineer",
    "Network Security Engineer": "Security Engineer",
    "Business Analyst": "Business Analyst",
    "ETL Developer": "Data Engineer",
    "Sales": "Sales",
    "HR": "HR",
    "Mechanical Engineer": "Mechanical Engineer",
    "Electrical Engineering": "Electrical Engineer",
    # MEDICAL
"Doctor": "Doctor",
"Nursing": "Nurse",

# PHARMACY
"Pharmacy": "Pharmacist",

# CIVIL
"Civil Engineering": "Civil Engineer",
"Construction": "Civil Engineer",

# ECE
"Electronics": "ECE Engineer",
"Embedded Systems": "Embedded Engineer",

# EEE
"Electrical": "Electrical Engineer",
"Power Systems": "EEE Engineer",

# MECHANICAL
"Mechanical": "Mechanical Engineer",
"Manufacturing": "Production Engineer",

# MARKETING
"Digital Marketing": "Digital Marketer",
"Social Media": "Social Media Manager",

"Teaching": "Teacher",
"Education": "Teacher",
"Faculty": "Lecturer",
"Trainer": "Trainer"

}


#Text processing

import re
def preprocess(text):
    text = text.lower()

    # keep + and #
    text = re.sub(r'[^a-zA-Z0-9+#.\s]', ' ', text)

    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_text(text):
    text = text.lower()
    # keep newline
    text = re.sub(r'[^a-zA-Z0-9\n\s+#.]', ' ', text)
    # remove only extra spaces (NOT newline)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def normalize_text(text):
    text = text.lower()

    for key, val in SYNONYMS.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        text = re.sub(pattern, val, text)

    return text

def clean_ocr_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

#skill extraction

def extract_skills(text):
    text = normalize_text(preprocess(text))
    found = set()

    for skill in SKILLS:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        
        if re.search(pattern, text):
            found.add(skill)

    return found

def skill_analysis(resume, jd):
    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(jd)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills.difference(resume_skills)

    if len(jd_skills) == 0:
        percent = 0
    else:
        percent = (len(matched) / len(jd_skills)) * 100

    return matched, missing, round(percent, 2)

from sklearn.metrics.pairwise import cosine_similarity

#similarity

def match_score(resume, jd):
    resume_clean = preprocess(resume)
    jd_clean = preprocess(jd)

    resume_vec = vectorizer.transform([resume_clean])
    jd_vec = vectorizer.transform([jd_clean])

    score = cosine_similarity(resume_vec, jd_vec)[0][0]

    return round(score * 100, 2)

#ml

def predict_role(resume):
    clean = preprocess(resume)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)

    role = le.inverse_transform(pred)[0]

    # apply mapping
    if role in CATEGORY_MAP:
        role = CATEGORY_MAP[role]

    return role

def refine_role(resume, role):
    skills = extract_skills(resume)

    best_role = role
    max_match = 0

    for r, required_skills in ROLE_RULES.items():
        match_count = len(set(required_skills) & skills)

        # choose role with highest matching skills
        if match_count > max_match and match_count >= 2:
            max_match = match_count
            best_role = r

    return best_role

#experience

def extract_experience(text):
    text = text.lower()

    # explicit years
    matches = re.findall(r'(\d+)\+?\s*(years|yrs|year)', text)
    if matches:
        return max([int(m[0]) for m in matches])
    
     # detect date ranges like 2019 - 2021
    exp_keywords = ["experience", "work", "employment", "intern", "company"]

    lines = text.split("\n")
    exp_years = []

    for line in lines:
        if any(word in line for word in exp_keywords):
            years = re.findall(r'(20\d{2})', line)
            if len(years) >= 2:
                exp_years.append(int(years[-1]) - int(years[0]))

    if exp_years:
        return max(exp_years)

    return 0


def get_required_experience(jd):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs|year)', jd.lower())

    if matches:
        return max([int(m[0]) for m in matches])
    
    return None

def experience_score(resume, jd):
    jd_lower = jd.lower()
    required = get_required_experience(jd)
    
    print(f"JD required experience: {required}")  # Debug log

    # 👉 ignore if fresher or not mentioned
    if "fresher" in jd_lower or required is None or required == 0:
        print("Experience: Not required (returning None)")  # Debug log
        return None

    candidate = extract_experience(resume)
    print(f"Candidate experience: {candidate} years")  # Debug log
    

    if candidate == 0:
        print("Experience: Candidate has 0 years (returning 0)")  # Debug log
        return 0

    if candidate >= required:
        print(f"Experience: Candidate meets requirement (returning 100)")  # Debug log
        return 100

    score = round((candidate / required) * 100, 2)
    print(f"Experience: Candidate has {candidate}/{required} years (returning {score})")  # Debug log
    return score

#file handling

def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()

            if content:
                text += content + "\n"
            else:
                # Try OCR if Tesseract is available
                if TESSERACT_AVAILABLE:
                    try:
                        image = page.to_image().original
                        # Improve OCR quality
                        image = image.convert('L')  # grayscale
                        ocr_text = pytesseract.image_to_string(image)
                        text += ocr_text + "\n"
                    except Exception as e:
                        print(f"⚠️  OCR failed for page: {e}")
                else:
                    print("⚠️  Skipping image-based page (Tesseract not available)")

    return text

from docx import Document

def extract_text_from_docx(file):
    doc = Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

def extract_text_from_image(file):
    if not TESSERACT_AVAILABLE:
        print("⚠️  Cannot extract text from image (Tesseract not available)")
        return ""
    
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"⚠️  Image extraction failed: {e}")
        return ""

def get_resume_text(file):
    # Handle both Streamlit and Flask file objects
    file_name = None
    
    # Try to get filename from Flask FileStorage
    if hasattr(file, 'filename') and file.filename:
        file_name = file.filename.lower()
    # Try to get from name attribute (Streamlit)
    elif hasattr(file, 'name'):
        file_name = file.name.lower()
    
    if not file_name:
        raise ValueError("Unable to determine file name. Please ensure the file has a proper name.")
    
    print(f"Processing file: {file_name}")  # Debug log

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    elif file_name.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file)

    else:
        raise ValueError(f"Unsupported file format: {file_name}. Supported formats: PDF, DOCX, JPG, PNG")

#name handling

def extract_name(text):
    lines = text.split("\n")

    for line in lines[:10]:
        line = line.strip()

        if not line:
            continue

        # skip emails
        if "@" in line:
            continue

        # skip lines with numbers
        if any(char.isdigit() for char in line):
            continue

        lower = line.lower()

        # skip unwanted words
        if any(word in lower for word in [
            "objective", "summary", "experience", "skills",
            "education", "project", "profile", "contact",
            "developer", "engineer", "student", "aspiring"
        ]):
            continue

        words = line.split()

        # stricter name rule
        if 2 <= len(words) <= 3:
            if all(word.isalpha() and word[0].isupper() for word in words):
                return " ".join(words)

    return "Unknown Candidate"

#final score

def final_score(similarity, skill_percent, exp_score=None):

    # If experience not used
    if exp_score is None:
        return round((similarity * 0.4) + (skill_percent * 0.6), 2)

    # If experience is used
    return round((similarity * 0.3) + (skill_percent * 0.4) + (exp_score * 0.3), 2)

#main pipeline

def analyze_resume(resume, jd):
    role = predict_role(resume)
    role = refine_role(resume, role)

    sim = match_score(resume, jd)
    matched, missing, skill_pct = skill_analysis(resume, jd)

    exp_score = experience_score(resume, jd)

    final = final_score(sim, skill_pct, exp_score)

    return {
        "Similarity %": sim,
        "Skill Match %": skill_pct,
        "Final Score %": final,
        "Matched Skills": list(matched),
        "Missing Skills": list(missing),
        "Predicted Role": role,
        "Experience %": exp_score
    }

def process_resumes(files, jd):
    results = []

    for file in files:
        resume_text = get_resume_text(file)
        name = extract_name(resume_text)

        if name == "Unknown Candidate":
            # Get filename from Flask or Streamlit file object
            if hasattr(file, 'filename') and file.filename:
                name = file.filename
            elif hasattr(file, 'name'):
                name = file.name
            else:
                name = "Unknown Candidate"

        resume_text = clean_text(resume_text)

        result = analyze_resume(resume_text, jd)

        result["Candidate Name"] = name
        results.append(result)

    # sort
    results = sorted(results, key=lambda x: x["Final Score %"], reverse=True)
    return results







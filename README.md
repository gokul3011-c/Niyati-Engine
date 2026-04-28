# 🧠 Niyati Engine  
### AI Resume Screening System

Niyati Engine is an intelligent AI-based resume screening system that automates candidate evaluation by analyzing resumes against a job description. It helps recruiters identify the best candidates efficiently using Natural Language Processing (NLP) and Machine Learning.

---

# 📌 Features

✔ Multi-resume upload (PDF, DOCX, Images)  
✔ TF-IDF based similarity scoring  
✔ Skill matching system  
✔ Role prediction using ML model  
✔ Experience scoring  
✔ Final ranking system  
✔ Cutoff-based filtering  
✔ Accepted / Rejected classification  
✔ Analytics (Pie Chart + Line Graph)  
✔ Download results as CSV  

---

# 🧠 How the System Works

Upload Resumes → Extract Text → Clean Text → Predict Role → Match with JD → Calculate Scores → Rank Candidates → Apply Cutoff → Display Results + Analytics

---

# ⚙️ Architecture Flow

User Input (UI)  
↓  
File Upload + Job Description  
↓  
Core Logic Processing  
↓  
Text Extraction  
↓  
Preprocessing (Cleaning)  
↓  
TF-IDF Vectorization  
↓  
Similarity Calculation  
↓  
Skill Matching  
↓  
Experience Scoring  
↓  
Final Score Calculation  
↓  
Ranking + Filtering  
↓  
UI Display + Analytics  

---

# 📂 Project Structure

Niyati Engine/  
│  
├── app.py  
├── core_logic.py  
├── model.pkl  
├── vectorizer.pkl  
├── label_encoder.pkl  
├── requirements.txt  

---

# 📦 Requirements

streamlit  
pandas  
numpy  
scikit-learn  
matplotlib  
pdfplumber  
python-docx  
pytesseract  
Pillow  

---

# 🚀 Installation & Setup

1. Clone Repository  
git clone <your-repo-link>  

2. Install Dependencies  
pip install -r requirements.txt  

3. Run Application  
streamlit run app.py  

---

# 🧠 Core Logic Explanation

get_resume_text(file) → Extract text from PDF/DOCX/Image  
clean_text(text) → Preprocess text  
predict_role(resume_text) → Predict role using ML  
refine_role(resume, role) → Improve prediction  
match_score(resume, jd) → Similarity calculation  
skill_analysis(resume, jd) → Skill matching  
experience_score(resume, jd) → Experience scoring  
final_score(sim, skill_pct, exp_score) → Final weighted score  
analyze_resume(resume, jd) → Complete pipeline  
process_resumes(files, jd) → Process all resumes  

---

# 🖥️ UI Logic

Input Panel → Upload + JD + Cutoff  
Analyze Button → Trigger processing  
Candidate Cards → Display results  
Ranking System → Sorted results  
Filtering → Accepted/Rejected  
Analytics → Pie + Line Graph  
Download → CSV export  

---

# 📊 Scoring System

Final Score = Similarity + Skill Match + Experience

---

# 💡 Use Cases

- Campus recruitment  
- Resume shortlisting  
- HR automation  
- Skill gap analysis  

---

# 🚀 Future Enhancements

- Recruiter dashboard  
- AI feedback system  
- Database integration  

---

# 🧠 Technologies

Python, Streamlit, Scikit-learn, NLP, OCR  

---

# 🏆 Conclusion

Niyati Engine automates resume screening using AI for faster and smarter hiring.

---

# 👨‍💻 Author

Gokul  
Engineering Student | AI Enthusiast

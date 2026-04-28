import streamlit as st
from core_logic import process_resumes
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Niyati Engine", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f1117, #111827);
    color: white;
}

.title {
    font-size: 40px;
    font-weight: bold;
    color: #00ffd5;
}

.section-title {
    font-size: 22px;
    margin-bottom: 10px;
    color: #00ffd5;
}

/* Left panel */
.left-panel {
    background: #161b22;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #222;
}

/* Button */
.stButton > button {
    width: 100%;
    background-color: #00ffd5;
    color: black;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🧠 Niyati Engine</div>', unsafe_allow_html=True)
st.write("AI Resume Screening System")
st.markdown("---")

# ---------------- LAYOUT ----------------
left, right = st.columns([1, 2], gap="large")

# ---------------- INPUT PANEL ----------------
with left:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Input Panel</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True)
    jd = st.text_area("Job Description", height=200)
    cutoff = st.slider("Cutoff Score", 0, 100, 70)
    analyze = st.button("🚀 Analyze")

    st.markdown('</div>', unsafe_allow_html=True)

    analytics_container = st.container()

# ---------------- CARD FUNCTION ----------------
def candidate_card(r, cutoff, rank=None, is_top=False):

    title = r['Candidate Name']

    if is_top:
        st.success("🏆 BEST MATCH")
        title += " 🏆 Top Candidate"

    if rank:
        title += f" (#{rank})"

    st.markdown("---")
    st.markdown(f"### {title}")

    score = r["Final Score %"]

    if score >= cutoff:
        score_color = "🟢"
    elif score >= cutoff * 0.8:
        score_color = "🟡"
    else:
        score_color = "🔴"

    cols = st.columns(2)

    with cols[0]:
        st.metric("Similarity", f"{r['Similarity %']}%")
        st.write(f"**Role:** {r['Predicted Role']}")

    with cols[1]:
        st.metric("Final Score", f"{score_color} {score}%")
        st.write(f"**Skill Match:** {r['Skill Match %']}%")

    st.progress(int(score))

    st.write("**Matched Skills:**")
    st.markdown(" ".join([f"`{s}`" for s in r["Matched Skills"]]))

    st.write("**Missing Skills:**")
    st.markdown(" ".join([f"`{s}`" for s in r["Missing Skills"]]))

# ---------------- OUTPUT PANEL ----------------
with right:

    if not analyze:
        st.info("👈 Upload resumes and click Analyze to see results")

    if analyze:

        if not uploaded_files or not jd.strip():
            st.warning("Please upload resumes and enter Job Description")

        else:
            results = process_resumes(uploaded_files, jd)

            results = sorted(results, key=lambda x: x["Final Score %"], reverse=True)

            accepted = [r for r in results if r["Final Score %"] >= cutoff]
            rejected = [r for r in results if r["Final Score %"] < cutoff]

            col1, col2, col3 = st.columns(3)
            col1.metric("Total", len(results))
            col2.metric("Accepted", len(accepted))
            col3.metric("Rejected", len(rejected))

            st.markdown("---")

            df = pd.DataFrame(results)
            st.download_button(
                "📥 Download Results",
                df.to_csv(index=False),
                "niyati_results.csv",
                "text/csv"
            )

            tab1, tab2 = st.tabs([
                f"✅ Accepted ({len(accepted)})",
                f"❌ Rejected ({len(rejected)})"
            ])

            with tab1:
                for i, r in enumerate(accepted, start=1):
                    candidate_card(r, cutoff, rank=i, is_top=(i == 1))

            with tab2:
                for r in rejected:
                    candidate_card(r, cutoff)

            # -------- ANALYTICS (LEFT SIDE) --------
            with analytics_container:

                st.markdown("---")
                st.markdown("### 📊 Analytics")

                labels = ["Accepted", "Rejected"]
                values = [len(accepted), len(rejected)]

                fig1, ax1 = plt.subplots()
                ax1.pie(values, labels=labels, autopct='%1.1f%%')
                ax1.set_title("Selection Distribution")

                st.pyplot(fig1)

                st.markdown("### 📈 Score vs Candidates")

                names = [r["Candidate Name"] for r in results]
                scores = [r["Final Score %"] for r in results]

                fig2, ax2 = plt.subplots()
                ax2.plot(names, scores, marker='o')
                ax2.set_xlabel("Candidates")
                ax2.set_ylabel("Final Score %")
                ax2.set_title("Candidate Score Trend")
                ax2.tick_params(axis='x', rotation=45)

                st.pyplot(fig2)
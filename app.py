import os
import streamlit as st
import matplotlib.pyplot as plt
from utils.pdf_reader import extract_text_from_pdf
from utils.similarity import calculate_similarity
from utils.skill_matcher import extract_skills
from utils.ats_score import calculate_ats_score
from utils.resume_suggestions import generate_resume_suggestions
from utils.gemini import generate_interview_questions
from utils.pdf_report import generate_pdf
import plotly.graph_objects as go
from utils.resume_rewriter import rewrite_resume
from utils.cover_letter import generate_cover_letter
from utils.mock_interview import (
    generate_mock_question,
    evaluate_answer
)
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)
# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.title("🤖 AI Career Assistant")
    st.write("---")
    st.success("✅ Resume Analysis")
    st.success("✅ ATS Score")
    st.success("✅ Skills Analysis")
    st.success("✅ AI Resume Suggestions")
    st.success("✅ Interview Questions")
    st.success("✅ Mock Interview")
    st.success("✅ Resume Rewriter")
    st.success("✅ Cover Letter Generator")
    st.success("✅ PDF Report")
    st.write("---")
    st.info(
        """
**Technologies**
• Python
• Streamlit
• Gemini AI
• ReportLab
• NLP
"""
    )
    st.write("---")
    st.caption("Version 1.0")
    st.caption("Developed by GADHAMSETTY HITHARTHA")
# -----------------------------
# Session State
# -----------------------------
defaults = {
    "analysis_done": False,
    "resume_text": "",
    "job_description": "",
    "similarity_score": 0.0,
    "ats_score": 0.0,
    "rewritten_resume": "",
    "cover_letter": "",
    "matched_skills": [],
    "missing_skills": [],
    "resume_suggestions": "",
    "interview_questions": "",
    "mock_question": "",
    "user_answer": "",
    "answer_feedback": "",
    "pdf_filename": "Resume_Analysis_Report.pdf"
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
# -----------------------------
# Title
# -----------------------------
st.markdown("""
# 🤖 AI Interview Preparation Assistant
### 🚀 AI-Powered Resume Analyzer & Interview Coach
Analyze your resume, calculate ATS score, discover missing skills,
receive AI-powered suggestions, generate interview questions,
rewrite your resume, and generate a professional cover letter.
""")
st.info(
    "💡 Upload your resume and a job description to receive a complete AI-powered career analysis."
)
st.divider()
# -----------------------------
# Resume Upload
# -----------------------------
st.header("📄 Upload Resume")
uploaded_file = st.file_uploader(
    "Choose your Resume (PDF)",
    type=["pdf"]
)
if uploaded_file:
    st.success("✅ Resume Uploaded Successfully!")
    resume_text = extract_text_from_pdf(uploaded_file)
    st.session_state.resume_text = resume_text
    st.write("### Resume Information")
    st.write("**Filename:**", uploaded_file.name)
    st.write("**Size:**", round(uploaded_file.size / 1024, 2), "KB")
    st.divider()
    st.subheader("📃 Extracted Resume")
    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )
# -----------------------------
# Job Description
# -----------------------------
st.divider()
st.header("💼 Job Description")
job_description = st.text_area(
    "Paste the Job Description",
    value=st.session_state.job_description,
    height=250,
    placeholder="""
Looking for an AI/ML Engineer
Skills:
Python
Machine Learning
Deep Learning
SQL
TensorFlow
NLP
Git
"""
)
st.session_state.job_description = job_description
# -----------------------------
# Analyze Button
# -----------------------------
analyze_button = st.button("🚀 Analyze Resume")
if analyze_button:
    if uploaded_file is None:
        st.warning("Please upload your resume.")
        st.stop()
    if st.session_state.job_description.strip() == "":
        st.warning("Please enter a Job Description.")
        st.stop()
    with st.spinner("Analyzing Resume..."):
        similarity_score = calculate_similarity(
            st.session_state.resume_text,
            st.session_state.job_description
        )
        resume_skills = extract_skills(st.session_state.resume_text)
        job_skills = extract_skills(st.session_state.job_description)
        matched_skills = sorted(
            resume_skills.intersection(job_skills)
        )
        missing_skills = sorted(
            job_skills.difference(resume_skills)
        )
        ats_score = calculate_ats_score(
            similarity_score,
            matched_skills,
            job_skills,
            st.session_state.resume_text
        )
        resume_suggestions = generate_resume_suggestions(
            st.session_state.resume_text,
            st.session_state.job_description
        )
        st.session_state.similarity_score = similarity_score
        st.session_state.ats_score = ats_score
        st.session_state.matched_skills = matched_skills
        st.session_state.job_skills = job_skills
        st.session_state.missing_skills = missing_skills
        st.session_state.resume_suggestions = resume_suggestions
        st.session_state.analysis_done = True
        generate_pdf(
        st.session_state.pdf_filename,
        similarity_score,
        ats_score,
        matched_skills,
        missing_skills,
        resume_suggestions,
        st.session_state.interview_questions,
        st.session_state.mock_question,
        st.session_state.answer_feedback,
        st.session_state.rewritten_resume,
        st.session_state.cover_letter
        )
    st.success("Analysis Completed Successfully!")
# ------------------------------------------
# Display Analysis Results
# ------------------------------------------
if st.session_state.analysis_done:
    st.markdown("## 📈 Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="
        background:#1E5631;
        padding:28px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 8px 20px rgba(0,0,0,0.35);
        ">
            <h3>🎯 Resume Match</h4>
            <h1>{st.session_state.similarity_score:.2f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="
        background:#1F4E79;
        padding:28px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 8px 20px rgba(0,0,0,0.35);
        ">
            <h3>📊 ATS Score</h4>
            <h1>{st.session_state.ats_score:.2f}/100</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="
        background:#7A4F01;
        padding:28px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 8px 20px rgba(0,0,0,0.35);
        ">
            <h3>✅ Skills</h4>
            <h1>{len(st.session_state.matched_skills)}</h2>
        </div>
        """, unsafe_allow_html=True)
    rating = (
        "Excellent" if st.session_state.ats_score >= 85 else
        "Very Good" if st.session_state.ats_score >= 70 else
        "Good" if st.session_state.ats_score >= 55 else
        "Improve"
    )
    with col4:
        st.markdown(f"""
        <div style="
        background:#5C2E91;
        padding:28px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 8px 20px rgba(0,0,0,0.35);
        ">
            <h3>🏆 Rating</h4>
            <h1>{rating}</h2>
        </div>
        """, unsafe_allow_html=True)
    st.divider()
    st.subheader("📊 ATS Performance Gauge")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.ats_score,
        title={"text": "ATS Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#00C853"},
            "steps": [
                {"range": [0, 40], "color": "#FF5252"},
                {"range": [40, 70], "color": "#FFD54F"},
                {"range": [70, 100], "color": "#66BB6A"}
            ]
        }
    ))
    fig.update_layout(
    width=500,
    height=350,
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="#0E1117",
    font=dict(color="white")
    )
    st.plotly_chart(
    fig,
    use_container_width=False,
    config={"displayModeBar": False}
    )
    st.divider()
    st.subheader("👨‍💼 Recruiter's Decision")
    if st.session_state.ats_score >= 85:
        st.success("🟢 Highly Recommended for Shortlisting")

    elif st.session_state.ats_score >= 70:
        st.info("🔵 Recommended for Interview")

    elif st.session_state.ats_score >= 55:
        st.warning("🟡 Needs Resume Improvements")

    else:
        st.error("🔴 Not Ready for Shortlisting")
    st.caption(
        "This recommendation is based on ATS score, keyword match, and resume quality."
    )
    st.divider()
    st.subheader("⭐ Overall Resume Score")
    # Skill Match Percentage
    total_skills = len(st.session_state.matched_skills) + len(st.session_state.missing_skills)
    if total_skills > 0:
        skills_score = (len(st.session_state.matched_skills) / total_skills) * 100
    else:
        skills_score = 100
    overall_score = (
        st.session_state.similarity_score * 0.4 +
        st.session_state.ats_score * 0.4 +
        skills_score * 0.2
    )
    overall_score = float(overall_score)
    st.progress(overall_score / 100)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "⭐ Overall Resume Score",
            f"{overall_score:.1f}%"
        )
    with col2:
        if overall_score >= 90:
            st.metric("Resume Quality", "Excellent")
        elif overall_score >= 80:
            st.metric("Resume Quality", "Very Good")
        elif overall_score >= 70:
            st.metric("Resume Quality", "Good")
        elif overall_score >= 60:
            st.metric("Resume Quality", "Average")
        else:
            st.metric("Resume Quality", "Needs Improvement")
    if overall_score >= 90:
        st.success("🏆 Grade: A+ (Excellent Resume)")

    elif overall_score >= 80:
        st.success("🥇 Grade: A (Very Good Resume)")

    elif overall_score >= 70:
        st.info("🥈 Grade: B (Good Resume)")

    elif overall_score >= 60:
        st.warning("🥉 Grade: C (Average Resume)")
    else:
        st.error("❌ Grade: D (Needs Improvement)")
    st.divider()
    st.markdown("## 🛠 Skills Analysis")
    st.caption("Comparison between your resume skills and the job requirements.")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("✅ Matched Skills")

        if st.session_state.matched_skills:
            for skill in sorted(st.session_state.matched_skills):
                st.markdown(f"""
                    <div style="
                    padding:10px;
                    margin-bottom:8px;
                    border-radius:10px;
                    background-color:#1E5631;
                    color:white;
                    font-weight:bold;">
                    ✅ {skill.title()}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No matching skills found.")
    with col2:
        st.markdown("❌ Missing Skills")
        if st.session_state.missing_skills:
            for skill in sorted(st.session_state.missing_skills):
                st.markdown(f"""
                    <div style="
                    padding:10px;
                    margin-bottom:8px;
                    border-radius:10px;
                    background-color:#7A1F1F;
                    color:white;
                    font-weight:bold;">
                    ❌ {skill.title()}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("🎉 No Missing Skills")
    st.divider()
    st.subheader("📊 Resume Statistics")
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(4,4))
        labels = ["Matched", "Missing"]
        values = [
            len(st.session_state.matched_skills),
            len(st.session_state.missing_skills)
        ]
        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Skills Distribution")
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots(figsize=(5,4))
        categories = ["Resume Match", "ATS Score"]
        scores = [
            st.session_state.similarity_score,
            st.session_state.ats_score
        ]
        ax.bar(categories, scores)
        ax.set_ylim(0,100)
        ax.set_ylabel("Score")
        ax.set_title("Resume Performance")
        st.pyplot(fig)
    st.divider()       
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Keyword Match")
        keyword_match = (
            len(st.session_state.matched_skills)
            / len(st.session_state.job_skills)
        ) * 100 if len(st.session_state.job_skills) else 0
        st.progress(int(keyword_match))
        st.write(f"**{keyword_match:.1f}%** of required keywords were found.")
    with col2:
        st.subheader("💪 Resume Strength")
        st.progress(int(st.session_state.ats_score))
        st.write(f"**Overall ATS Score:** {st.session_state.ats_score:.2f}/100")
        st.subheader("👨‍💼 Recruiter's Decision")
        if st.session_state.ats_score >= 85:
            st.success("✅ Shortlist for Interview")
        elif st.session_state.ats_score >= 70:
            st.info("🟢 Good Candidate")
        elif st.session_state.ats_score >= 55:
            st.warning("🟡 Needs Resume Improvements")
        else:
            st.error("🔴 Resume Not Ready")
    st.divider()
    with st.expander("💡 AI Resume Suggestions", expanded=True):
        st.info(st.session_state.resume_suggestions)
    st.divider()
    with st.expander("🤖 AI Interview Questions", expanded=False):
        generate_questions = st.button("Generate AI Interview Questions")
        if generate_questions:
            if not st.session_state.resume_text:
                st.warning("⚠️ Please upload your resume first.")
            elif not st.session_state.job_description:
                st.warning("⚠️ Please enter a job description first.")
            else:
                with st.spinner("🤖 Generating Interview Questions..."):
                    questions = generate_interview_questions(
                        st.session_state.resume_text,
                        st.session_state.job_description
                    )
                    st.session_state.interview_questions = questions
                    generate_pdf(
                        st.session_state.pdf_filename,
                        st.session_state.similarity_score,
                        st.session_state.ats_score,
                        st.session_state.matched_skills,
                        st.session_state.missing_skills,
                        st.session_state.resume_suggestions,
                        questions,
                        st.session_state.mock_question,
                        st.session_state.answer_feedback,
                        st.session_state.rewritten_resume,
                        st.session_state.cover_letter
                    )
                    st.success("✅ Interview Questions Generated Successfully!")
        if st.session_state.interview_questions != "":
            st.markdown(st.session_state.interview_questions)
    st.divider()
    with st.expander("🎤 AI Mock Interview", expanded=False):
        st.write("Practice AI-generated interview questions and receive feedback.")
        if st.button("🎤 Start Mock Interview"):
            if not st.session_state.resume_text:
                st.warning("⚠️ Please upload your resume first.")
            elif not st.session_state.job_description:
                st.warning("⚠️ Please enter a job description first.")
            else:
                with st.spinner("🎤 Preparing Mock Interview..."):
                    question = generate_mock_question(
                        st.session_state.resume_text,
                        st.session_state.job_description
                    )
                    st.session_state.mock_question = question
                    generate_pdf(
                        st.session_state.pdf_filename,
                        st.session_state.similarity_score,
                        st.session_state.ats_score,
                        st.session_state.matched_skills,
                        st.session_state.missing_skills,
                        st.session_state.resume_suggestions,
                        st.session_state.interview_questions,
                        st.session_state.mock_question,
                        st.session_state.answer_feedback,
                        st.session_state.rewritten_resume,
                        st.session_state.cover_letter
                    )
                    st.success("✅ Mock Interview Ready!")
        if st.session_state.mock_question != "":
            st.subheader("🎯 Interview Question")
            st.write(st.session_state.mock_question)
            answer = st.text_area(
                "Your Answer",
                key="user_answer",
                height=180
            )
            if st.button("Evaluate My Answer"):
                with st.spinner("🤖 Evaluating Your Answer..."):
                    feedback = evaluate_answer(
                        st.session_state.mock_question,
                        answer
                    )
                    st.session_state.answer_feedback = feedback
                    generate_pdf(
                        st.session_state.pdf_filename,
                        st.session_state.similarity_score,
                        st.session_state.ats_score,
                        st.session_state.matched_skills,
                        st.session_state.missing_skills,
                        st.session_state.resume_suggestions,
                        st.session_state.interview_questions,
                        st.session_state.mock_question,
                        st.session_state.answer_feedback,
                        st.session_state.rewritten_resume,
                        st.session_state.cover_letter
                    )
                    st.success("✅ Answer Evaluated Successfully!")
        if st.session_state.answer_feedback != "":
            st.subheader("🤖 AI Feedback")
            st.success(st.session_state.answer_feedback)
    st.divider()
    with st.expander("✨ AI Resume Rewriter", expanded=False):
        if st.button("✨ Rewrite Resume"):
            if not st.session_state.resume_text:
                st.warning("⚠️ Please upload your resume first.")
            elif not st.session_state.job_description:
                st.warning("⚠️ Please enter a job description first.")
            else:
                with st.spinner("✨ Rewriting Resume..."):
                    rewritten = rewrite_resume(
                        st.session_state.resume_text,
                        st.session_state.job_description
                    )
                st.session_state.rewritten_resume = rewritten
                generate_pdf(
                    st.session_state.pdf_filename,
                    st.session_state.similarity_score,
                    st.session_state.ats_score,
                    st.session_state.matched_skills,
                    st.session_state.missing_skills,
                    st.session_state.resume_suggestions,
                    st.session_state.interview_questions,
                    st.session_state.mock_question,
                    st.session_state.answer_feedback,
                    st.session_state.rewritten_resume,
                    st.session_state.cover_letter
                )
                st.success("✅ Resume Rewritten Successfully!")
        if st.session_state.rewritten_resume != "":
            st.subheader("Rewritten Resume")
            st.text_area(
                "ATS Optimized Resume",
                st.session_state.rewritten_resume,
                height=500
            )
    st.divider()
    with st.expander("📄 AI Cover Letter Generator", expanded=False):
        st.write(
            "Generate a professional cover letter tailored to the selected job description."
        )
        if st.button("📄 Generate Cover Letter"):
            if not st.session_state.resume_text:
                st.warning("⚠️ Please upload your resume first.")
            elif not st.session_state.job_description:
                st.warning("⚠️ Please enter a job description first.")
            else:
                with st.spinner("📝 Writing Cover Letter..."):
                    cover_letter = generate_cover_letter(
                        st.session_state.resume_text,
                        st.session_state.job_description
                    )
                st.session_state.cover_letter = cover_letter
                generate_pdf(
                    st.session_state.pdf_filename,
                    st.session_state.similarity_score,
                    st.session_state.ats_score,
                    st.session_state.matched_skills,
                    st.session_state.missing_skills,
                    st.session_state.resume_suggestions,
                    st.session_state.interview_questions,
                    st.session_state.mock_question,
                    st.session_state.answer_feedback,
                    st.session_state.rewritten_resume,
                    st.session_state.cover_letter
                )
                st.success("✅ Cover Letter Generated Successfully!")
        if st.session_state.cover_letter != "":
            st.subheader("Generated Cover Letter")
            st.text_area(
                "Cover Letter",
                st.session_state.cover_letter,
                height=500
            )
    st.divider()
    with st.expander("📥 Download Report", expanded=False):
        generate_pdf(
            st.session_state.pdf_filename,
            st.session_state.similarity_score,
            st.session_state.ats_score,
            st.session_state.matched_skills,
            st.session_state.missing_skills,
            st.session_state.resume_suggestions,
            st.session_state.interview_questions,
            st.session_state.mock_question,
            st.session_state.answer_feedback,
            st.session_state.rewritten_resume,
            st.session_state.cover_letter
        )
        with open(st.session_state.pdf_filename, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Resume Analysis Report",
                data=pdf_file,
                file_name="AI_Resume_Analysis_Report.pdf",
                mime="application/pdf"
            )                
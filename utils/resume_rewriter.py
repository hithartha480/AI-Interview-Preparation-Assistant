import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def rewrite_resume(resume_text, job_description):
    prompt = f"""
You are a professional ATS Resume Expert and Technical Recruiter.
Your task is to improve the resume ONLY.
========================
ORIGINAL RESUME
========================
{resume_text}
========================
JOB DESCRIPTION
========================
{job_description}
STRICT RULES (MUST FOLLOW):
1. NEVER invent any information.
2. NEVER change project names.
3. NEVER replace one project with another.
4. NEVER create fake internships, jobs, certifications, companies, or achievements.
5. NEVER modify technologies unless they already exist in the resume.
6. Preserve every fact exactly as written.
7. Improve only:
   - Grammar
   - Professional wording
   - ATS optimization
   - Bullet points
   - Formatting
8. Add relevant ATS keywords ONLY if they naturally fit the existing experience.
9. Keep the resume truthful.
10. If a project is named "Personal Expense Tracker", it must remain "Personal Expense Tracker" and its description should only be improved—not replaced with another project.
Return ONLY the rewritten resume in clean Markdown.
Do not include explanations, notes, or comments.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return """
    ⚠️ AI Resume Rewriter is temporarily unavailable.
    Possible reasons:
    • Gemini free quota exceeded.
    • Internet connection issue.
    • Invalid API key.
    Please try again later.
    """
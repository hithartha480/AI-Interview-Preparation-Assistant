import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def generate_cover_letter(resume_text, job_description):
    prompt = f"""
You are a professional HR recruiter.
Using the resume and job description below, generate a professional cover letter.
Resume:
{resume_text}
Job Description:
{job_description}
Requirements:
- Professional tone
- Around 300-400 words
- Mention relevant skills and projects
- Tailor it to the job description
- Do not invent fake experience
- Return only the cover letter
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        if "quota" in str(e).lower():
            return """
    ⚠️ Free Gemini API limit reached.
    Please try again after a few minutes.
    """
        return """
    ⚠️ AI Cover Letter Generator is temporarily unavailable.
    Possible reasons:
    • Gemini free quota exceeded.
    • Internet connection issue.
    • Invalid API key.
    Please try again later.
    """
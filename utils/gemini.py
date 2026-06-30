import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def generate_interview_questions(resume_text, job_description):
    prompt = f"""
You are a Senior Technical Interviewer.
Based on the resume and job description, generate interview questions.
Resume:
{resume_text}
Job Description:
{job_description}
Return the output exactly in this format:
## Technical Questions
1.
2.
3.
4.
5.
## Project Questions
6.
7.
8.
## HR Questions
9.
10.
Only generate questions.
Do not provide answers.
Do not explain anything.
"""
    try:
        response = model.generate_content(prompt)
        if response.text is None:
            return "Unable to generate interview questions."
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return """
    ⚠️ AI Interview Questions are temporarily unavailable.
    Possible reasons:
    • Gemini free quota exceeded.
    • Internet connection issue.
    • Invalid API key.
    Please try again later.
    """

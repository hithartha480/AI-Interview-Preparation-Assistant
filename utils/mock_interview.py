import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def generate_mock_question(resume_text, job_description):
    prompt = f"""
You are a Senior Technical Interviewer.
Based on the following resume and job description,
generate ONLY ONE interview question.
Resume:
{resume_text}
Job Description:
{job_description}
Rules:
- Ask only one question.
- Make it professional.
- Do not provide the answer.
- Return only the question.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return """
    ⚠️ AI Mock Interview is temporarily unavailable.
    Possible reasons:
    • Gemini free quota exceeded.
    • Internet connection issue.
    • Invalid API key.
    Please try again later.
    """
def evaluate_answer(question, answer):
    prompt = f"""
You are a Senior Technical Interviewer.
Evaluate the candidate's interview answer.
Question:
{question}
Candidate Answer:
{answer}
Return the evaluation in exactly this format:
Score: X/10
Strengths:
- ...
- ...
Improvements:
- ...
- ...
Keep the feedback concise and professional.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return """
    ⚠️ AI Feedback is temporarily unavailable.
    Possible reasons:
    • Gemini free quota exceeded.
    • Internet connection issue.
    • Invalid API key.
    Please try again later.
    """   
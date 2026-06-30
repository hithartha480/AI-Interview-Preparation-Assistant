import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def get_rule_based_suggestions(resume_text):
    resume = resume_text.lower()
    suggestions = []
    if "github" not in resume:
        suggestions.append("• Add your GitHub profile.")
    if "linkedin" not in resume:
        suggestions.append("• Add your LinkedIn profile.")
    if "project" not in resume:
        suggestions.append("• Include at least 2 strong projects.")
    if "certification" not in resume and "certificate" not in resume:
        suggestions.append("• Add relevant certifications.")
    if "experience" not in resume:
        suggestions.append("• Mention internships or practical experience.")
    if "skill" not in resume:
        suggestions.append("• Add a dedicated Skills section.")
    if len(resume.split()) < 250:
        suggestions.append("• Expand your resume with more technical details.")
    return suggestions
def generate_resume_suggestions(resume_text, job_description):
    prompt = f"""
You are a professional ATS Resume Reviewer.
Compare the resume with the job description.
Resume:
{resume_text}
Job Description:
{job_description}
Provide exactly 6 ATS-friendly suggestions.
Rules:
- Mention only improvements.
- Keep each suggestion under 20 words.
- Use bullet points.
- Do not explain.
- Do not add introductions or conclusions.
"""
    try:
        response = model.generate_content(prompt)
        rule_suggestions = get_rule_based_suggestions(resume_text)
        result = ""
        if rule_suggestions:
            result += "### Rule-Based Suggestions\n\n"
            result += "\n".join(rule_suggestions)
            result += "\n\n"
        result += "### AI Suggestions\n\n"
        result += response.text
        return result
    except Exception as e:
        print("Gemini Error:", e)
        rule_suggestions = get_rule_based_suggestions(resume_text)
        if rule_suggestions:
            return (
                "### Rule-Based Suggestions\n\n"
                + "\n".join(rule_suggestions)
                + "\n\n⚠️ AI suggestions are temporarily unavailable."
            )
        return "⚠️ AI suggestions are temporarily unavailable. Please try again later."
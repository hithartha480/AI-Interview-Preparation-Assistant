def calculate_ats_score(
    similarity_score,
    matched_skills,
    job_skills,
    resume_text
):
    score = 0

    resume = resume_text.lower()

    # ----------------------------
    # Resume Similarity (40 Marks)
    # ----------------------------
    similarity_marks = similarity_score * 0.40
    score += similarity_marks

    # ----------------------------
    # Skills Match (35 Marks)
    # ----------------------------
    if len(job_skills) > 0:
        skill_percentage = len(matched_skills) / len(job_skills)
        skill_marks = skill_percentage * 35
        score += skill_marks

    # ----------------------------
    # Resume Sections (15 Marks)
    # ----------------------------
    section_marks = 0

    if "project" in resume:
        section_marks += 3

    if "education" in resume or "b.tech" in resume or "bachelor" in resume:
        section_marks += 3

    if "skills" in resume:
        section_marks += 3

    if "experience" in resume:
        section_marks += 3

    if "certification" in resume or "certificate" in resume:
        section_marks += 3

    score += section_marks

    # ----------------------------
    # Contact Information (5 Marks)
    # ----------------------------
    contact_marks = 0

    if "@" in resume:
        contact_marks += 2

    if "+" in resume:
        contact_marks += 1

    if "linkedin" in resume:
        contact_marks += 1

    if "github" in resume:
        contact_marks += 1

    score += contact_marks

    # ----------------------------
    # Resume Length (5 Marks)
    # ----------------------------
    words = len(resume.split())

    if 250 <= words <= 700:
        score += 5
    elif 150 <= words < 250:
        score += 3
    elif words > 700:
        score += 2

    score = min(score, 100)

    return round(score, 2)
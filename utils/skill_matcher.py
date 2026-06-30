import re

def extract_skills(text):

    skills_database = [
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "mysql",
        "mongodb",
        "html",
        "css",
        "javascript",
        "react",
        "nodejs",
        "git",
        "github",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "nlp",
        "tensorflow",
        "keras",
        "pytorch",
        "opencv",
        "streamlit",
        "flask",
        "django",
        "data structures",
        "algorithms",
        "aws",
        "docker",
        "linux"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills_database:

        if re.search(r"\b" + re.escape(skill) + r"\b", text):

            found_skills.append(skill)

    return set(found_skills)
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the AI model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, job_description):
    # Convert text into embeddings
    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([job_description])

    # Calculate similarity
    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    return round(score * 100, 2)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


def compute_similarity(text1: str, text2: str) -> float:
    """
    Computes keyword-based similarity using TF-IDF + cosine similarity.
    Returns a percentage (0–100).
    """
    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    return round(score * 100, 2)


semantic_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_semantic_similarity(text1: str, text2: str) -> float:
    """
    Computes semantic similarity using SBERT embeddings.
    Returns a percentage (0–100).
    """
    embeddings = semantic_model.encode([text1, text2])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(score * 100, 2)

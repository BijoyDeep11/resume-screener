from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    return round(score * 100, 2)

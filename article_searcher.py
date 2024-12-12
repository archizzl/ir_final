from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

with open('articles.json') as f:
    articles = json.load(f)

corpus = [f"{article['articleTitle']} {article['articleAuthor']} {article['articleText']}" for article in articles]
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(corpus)

def search_articles(query, tfidf_matrix, articles, vectorizer, output_file="search_results.txt"):
    query_vec = vectorizer.transform([query])

    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    ranked_indices = np.argsort(-scores)
    ranked_articles = [
        (scores[i], articles[i]["articleTitle"], articles[i]["articleAuthor"], articles[i]["articleText"])
        for i in ranked_indices if scores[i] > 0
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        for rank, (score, title, author, text) in enumerate(ranked_articles, 1):
            sanitized_title = title.encode("ascii", errors="ignore").decode("ascii")
            sanitized_author = author.encode("ascii", errors="ignore").decode("ascii")
            sanitized_text = text.encode("ascii", errors="ignore").decode("ascii")

            f.write(f"Rank {rank} (Score: {score:.4f}):\n")
            f.write(f"Title: {sanitized_title}\n")
            f.write(f"Author: {sanitized_author}\n")
            f.write(f"Text: {sanitized_text}\n\n")
    
    print(f"Search results saved to {output_file}")

query = input("Enter search query: ")
search_articles(query, tfidf_matrix, articles, vectorizer)

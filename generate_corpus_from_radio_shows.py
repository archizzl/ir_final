import csv
import re
from collections import Counter
import json

# Define stopwords
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

# Tokenization function for multiple radio show data
def tokenize_radio_show(shows_data, corpus_file="corpus.csv"):
    corpus = Counter()

    # Tokenize a string into word types
    def tokenize_field(field, is_title=False):
        tokens = []
        if is_title:
            tokens.append(field.lower())
        words = re.findall(r"\b\w+(?:[-']\w+)*\b", field)
        i = 0
        while i < len(words):
            word = words[i]
            word_lower = word.lower()

            if word.istitle() and i < len(words) - 1 and words[i + 1].istitle():
                phrase = word
                j = i + 1
                while j < len(words) and words[j].istitle():
                    phrase += f" {words[j]}"
                    j += 1
                tokens.append(phrase.lower())
                i = j
                continue

            if word_lower not in stopwords or word.istitle():
                tokens.append(word_lower)
            i += 1

        return tokens

    # Process each show
    for show in shows_data:
        corpus.update(tokenize_field(show["title"], is_title=True))
        for key in ["bio", "dj", "genre", "episode", "description"]:
            if show.get(key):
                corpus.update(tokenize_field(show[key]))

        for song in show.get("songs", []):
            for key, value in song.items():
                if key != "url" and value:
                    corpus.update(tokenize_field(value))

    # Write to the CSV file
    with open(corpus_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="`")
        for word, count in corpus.items():
            writer.writerow([word, count])

# Example usage
with open('unique_shows_since_2022.json') as f:
    shows = json.load(f)
    tokenize_radio_show(shows)
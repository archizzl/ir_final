import csv
import re
from collections import Counter
import json

# https://gist.github.com/sebleier/554280
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

def tokenize_and_update_corpus(articles, corpus_file="corpus.csv"):
    """
    Tokenizes the text of articles, counts word occurrences, and updates a corpus CSV file.

    Args:
        articles (list): A list of dictionaries containing articles.
        corpus_file (str): Path to the CSV file to update.
    """
    def tokenize_text(text):
        tokens = []
        words = re.findall(r"\b\w+\b|(?:\b[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*)+)", text)  # Extract individual words and capitalized sequences

        for i, word in enumerate(words):
            word_lower = word.lower()
            # Handle multi-word capitalized sequences
            if word.istitle() and i < len(words) - 1 and words[i + 1].istitle():
                combined = word
                while i < len(words) - 1 and words[i + 1].istitle():
                    combined += f" {words[i + 1]}"
                    i += 1
                # Only include sequences with less than three spaces
                if combined.count(" ") < 3:
                    tokens.append(combined)
                    tokens.extend([w.lower() for w in combined.split() if w.lower() not in stopwords])
            elif word_lower not in stopwords or (word.istitle() and (i > 0 and words[i - 1].istitle() or i < len(words) - 1 and words[i + 1].istitle())):
                tokens.append(word_lower)
        return tokens

    word_counter = Counter()

    for article in articles:
        # Tokenize article text
        word_counter.update(tokenize_text(article["articleText"]))

        # Tokenize article author
        author = article["articleAuthor"]
        if not any(char.isdigit() for char in author):
            word_counter[author] += 1
            word_counter.update(author.lower().split())

        # Tokenize article title by splitting on spaces
        title_tokens = article["articleTitle"].split()
        word_counter.update([word.lower() for word in title_tokens])

    # Read existing corpus.csv (if it exists) into a Counter
    existing_counter = Counter()
    try:
        with open(corpus_file, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter="`")
            for row in reader:
                if len(row) == 2:
                    word, count = row
                    existing_counter[word] = int(count)
    except FileNotFoundError:
        pass

    # Merge new counts with existing counts
    for word, count in word_counter.items():
        existing_counter[word] += count

    # Write updated counts back to corpus.csv
    with open(corpus_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="`")
        for word, count in existing_counter.most_common():
            writer.writerow([word, count])

with open('articles.json') as f:
    articles = json.load(f)
    tokenize_and_update_corpus(articles)

import csv
import json
import re
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def prune_corpus(corpus_file):
    pruned_rows = []

    with open(corpus_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="`")
        for row in reader:
            if len(row) != 2:
                continue  # Skip malformed rows

            word, count = row[0], row[1]

            try:
                count = int(count)
            except ValueError:
                continue  # Skip rows with non-integer counts

            # Pruning conditions
            if word.lower().startswith("wrbb 104.9fm"):
                continue
            if len(word) == 1:
                continue
            if not re.search(r"[a-zA-Z]", word):
                continue
            if word.lower() in stopwords:
                continue
            if word.count(" ") > 2 and count < 3:
                continue

            pruned_rows.append([word, count])

    # Write the pruned corpus back to the file
    with open(corpus_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="`")
        writer.writerows(pruned_rows)

prune_corpus('corpus.csv')
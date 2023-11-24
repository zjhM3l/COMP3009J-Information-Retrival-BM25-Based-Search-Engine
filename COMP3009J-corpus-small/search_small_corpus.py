import os
import re
import string
from math import log
from files.porter import PorterStemmer  # Assume this is the porter stemmer in your porter.py

# Step 1: Load stop words
with open('files/stopwords.txt', 'r') as f:
    stop_words = set(f.read().split())

# Step 2: Initialize the Porter Stemmer
stemmer = PorterStemmer()


# Step 3: Define a function to extract the documents, perform stopword removal and stemming
def process_documents():
    result = []
    for filename in os.listdir('documents'):
        with open(f'documents/{filename}', 'r') as f:
            # Read the document
            doc = f.read().lower()

            # Tokenize the document
            doc = re.sub('[' + string.punctuation + ']', ' ', doc)  # replace punctuation with spaces
            terms = doc.split()

            # Perform stopword removal
            terms = [term for term in terms if term not in stop_words]

            # Perform stemming
            terms = [stemmer.stem(term) for term in terms]

            result.append((filename, terms))
    return result


# Step 4: Load index from file if possible
index_filename = 'result.txt'
if os.path.exists(index_filename):
    result = []
    try:
        with open(index_filename, 'r') as f:
            for line in f:
                items = line.strip().split(": ")
                if len(items) == 2:  # Check if the line has the correct format
                    result.append((items[0], items[1].split()))
                else:
                    print(f"Skipping line due to incorrect format: {line}")
    except Exception as e:
        print(f"Failed to load index from {index_filename} due to {e}. Processing documents again...")
        result = process_documents()
else:
    result = process_documents()

# Step 5: Write the result to 'result.txt'
with open('result.txt', 'w') as f:
    for filename, terms in result:
        f.write(f'{filename}: {" ".join(terms)}\n')

# Clear the results file
open('results.txt', 'w').close()

# BM25 parameters
k1 = 1
b = 0.75

# Calculate average document length
avg_doc_len = sum(len(terms) for _, terms in result) / len(result)


# Calculate document frequencies for each term
doc_freqs = {}
for _, terms in result:
    for term in set(terms):
        doc_freqs[term] = doc_freqs.get(term, 0) + 1

# Calculate BM25 scores for each query
with open('files/queries.txt', 'r') as f:
    queries = [line.strip().split(" ", 1) for line in f]
queries = [(q_id, re.sub('[' + string.punctuation + ']', ' ', q_content).split()) for q_id, q_content in queries]

for q_id, q_terms in queries:
    scores = []

    for doc_id, terms in result:
        score = 0

        for term in set(q_terms):
            if term not in doc_freqs:
                continue

            # Calculate term frequency in the document
            tf = terms.count(term)

            # Calculate BM25 score
            idf = log((len(result) - doc_freqs[term] + 0.5) / (doc_freqs[term] + 0.5))
            tf_component = ((k1 + 1) * tf) / (k1 * ((1 - b) + b * (len(terms) / avg_doc_len)) + tf)
            score += idf * tf_component

        scores.append((doc_id, score))

    # Sort scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Write scores to 'results.txt'
    with open('results.txt', 'a') as f:
        for rank, (doc_id, score) in enumerate(scores, start=1):
            f.write(f"{q_id} Q0 {doc_id} {rank} {score:.4f} 17205961\n")








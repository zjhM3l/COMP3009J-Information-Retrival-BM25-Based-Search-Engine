import os
import re
import string
from math import log
import time
from files.porter import PorterStemmer  # Assume this is the porter stemmer in your porter.py

# Step 1: Load stop words
with open('files/stopwords.txt', 'r') as f:
    stop_words = set(f.read().split())

# Step 2: Initialize the Porter Stemmer
stemmer = PorterStemmer()

# New inverted index structure
inverted_index = {}


# Step 3: Define a function to extract the documents, perform stopword removal and stemming
def process_documents(directory):
    print(f"Processing documents in {directory}...")
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if the file is a text file by looking for 'GX' in the filename
            if 'GX' not in filename:
                print(f"Skipping non-text file: {filename}")
                continue

            print(f"Processing file {os.path.join(root, filename)}...")

            with open(os.path.join(root, filename), 'r', encoding='utf-8', errors='ignore') as f:
                # Read the document
                doc = f.read().lower()

                # Tokenize the document
                doc = re.sub('[' + string.punctuation + ']', ' ', doc)  # replace punctuation with spaces
                terms = doc.split()

                # Perform stopword removal and stemming
                terms = [stemmer.stem(term) for term in terms if term not in stop_words]

                # Add terms to the inverted index
                for term in terms:
                    if term not in inverted_index:
                        inverted_index[term] = {filename: 1}
                    elif filename not in inverted_index[term]:
                        inverted_index[term][filename] = 1
                    else:
                        inverted_index[term][filename] += 1

    print(f"Finished processing documents in {directory}. Processed {len(inverted_index)} unique terms.")
    return inverted_index


# Step 4: Load index from file if possible
index_filename = 'result.txt'
if os.path.exists(index_filename):
    inverted_index = {}
    try:
        with open(index_filename, 'r') as f:
            for line in f:
                term, postings_list = line.strip().split(": ")
                postings_dict = dict(item.split(":") for item in postings_list.split())
                inverted_index[term] = postings_dict
    except Exception as e:
        print(f"Failed to load index from {index_filename} due to {e}. Processing documents again...")
        start = time.time()
        inverted_index = process_documents('documents')
        end = time.time()
        print(f"Time taken to process documents: {end - start} seconds")
else:
    start = time.time()
    inverted_index = process_documents('documents')
    end = time.time()
    print(f"Time taken to process documents: {end - start} seconds")


# Step 5: Write the inverted index to 'result.txt'
with open('result.txt', 'w', encoding='utf-8') as f:
    for term, postings_dict in inverted_index.items():
        postings_list = " ".join(f"{docID}:{freq}" for docID, freq in postings_dict.items())
        f.write(f'{term}: {postings_list}\n')

# Clear the results file
open('results.txt', 'w').close()

# BM25 parameters
k1 = 1.2
b = 0.75

# Calculate average document length
total_length = sum(freq for term in inverted_index for freq in inverted_index[term].values())
num_docs = len(set(docID for term in inverted_index for docID in inverted_index[term].keys()))
avg_doc_len = total_length / num_docs

# Calculate BM25 scores for each query
with open('files/queries.txt', 'r') as f:
    queries = [line.strip().split(" ", 1) for line in f]
queries = [(q_id, re.sub('[' + string.punctuation + ']', ' ', q_content).split()) for q_id, q_content in queries]

for q_id, q_terms in queries:
    scores = []

    for doc_id, terms in inverted_index.items():
        score = 0

        for term in set(q_terms):
            if term not in inverted_index:
                continue

            # Calculate term frequency in the document
            tf = inverted_index[term].get(doc_id, 0)

            # Calculate BM25 score
            idf = log((len(inverted_index) - len(inverted_index[term]) + 0.5) / (len(inverted_index[term]) + 0.5))
            tf_component = ((k1 + 1) * tf) / (k1 * ((1 - b) + b * (sum(len(postings) for postings in inverted_index.values()) / len(inverted_index))) + tf)
            score += idf * tf_component

        scores.append((doc_id, score))

    # Sort scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Write scores to 'results.txt'
    with open('results.txt', 'a') as f:
        for rank, (doc_id, score) in enumerate(scores, start=1):
            f.write(f"{q_id} Q0 {doc_id} {rank} {score:.4f} 17205961\n")
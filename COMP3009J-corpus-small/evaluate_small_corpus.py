import os
import numpy as np

# Load results
results = {}
with open('results.txt', 'r') as f:
    for line in f:
        q_id, _, doc_id, rank, _, _ = line.strip().split()
        if q_id not in results:
            results[q_id] = []
        results[q_id].append((doc_id, int(rank)))

# Load relevance judgments
qrels = {}
with open('files/qrels.txt', 'r') as f:
    for line in f:
        q_id, _, doc_id, rel = line.strip().split()
        if q_id not in qrels:
            qrels[q_id] = {}
        qrels[q_id][doc_id] = int(rel)


# Calculate evaluation metrics
precisions = []
recalls = []
p_at_10s = []
r_precisions = []
aps = []
bprefs = []

for q_id, res in results.items():
    if q_id not in qrels:
        continue

    rel_docs = set(doc_id for doc_id, rel in qrels[q_id].items() if rel > 0)
    res_docs = [doc_id for doc_id, _ in res]

    # Calculate precision and recall
    relevant_retrieved_docs = set(res_docs) & rel_docs
    precision = len(relevant_retrieved_docs) / len(res_docs)
    recall = len(relevant_retrieved_docs) / len(rel_docs) if rel_docs else 0
    precisions.append(precision)
    recalls.append(recall)

    # Calculate P@10
    p_at_10 = len(set(res_docs[:10]) & rel_docs) / 10
    p_at_10s.append(p_at_10)

    # Calculate R-precision
    r_precision = len(set(res_docs[:len(rel_docs)]) & rel_docs) / len(rel_docs) if rel_docs else 0
    r_precisions.append(r_precision)

    # Calculate MAP
    precisions_at_k = [len(set(res_docs[:k+1]) & rel_docs) / (k+1) for k in range(len(res_docs))]
    ap = np.mean(precisions_at_k) if precisions_at_k else 0
    aps.append(ap)

    # Calculate bpref
    non_rel_docs = len(res_docs) - len(rel_docs)
    rank_rel = [rank for doc_id, rank in res if doc_id in rel_docs]
    rank_non_rel = [rank for doc_id, rank in res if doc_id not in rel_docs]
    bpref = sum((1 - len([r for r in rank_non_rel if r < r_rel]) / non_rel_docs) for r_rel in rank_rel) / len(rel_docs) if rel_docs else 0
    bprefs.append(bpref)

# Print evaluation metrics
print(f'Precision: {np.mean(precisions)}')
print(f'Recall: {np.mean(recalls)}')
print(f'P@10: {np.mean(p_at_10s)}')
print(f'R-precision: {np.mean(r_precisions)}')
print(f'MAP: {np.mean(aps)}')
print(f'bpref: {np.mean(bprefs)}')


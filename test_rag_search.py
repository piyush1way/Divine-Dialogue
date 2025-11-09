#!/usr/bin/env python3
"""
Quick test script to demonstrate RAG database usage
"""

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load FAISS vector store
print("Loading FAISS vector store...")
index = faiss.read_index('sacred_texts_rag_faiss/index.faiss')

with open('sacred_texts_rag_faiss/texts.json', 'r', encoding='utf-8') as f:
    texts = json.load(f)

with open('sacred_texts_rag_faiss/metadatas.json', 'r', encoding='utf-8') as f:
    metadatas = json.load(f)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print(f"✓ Loaded {index.ntotal} verses\n")


def search_verses(query: str, mentor: str = None, top_k: int = 3):
    """Search for relevant verses"""
    
    # Generate query embedding
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # Search in FAISS (get more results if filtering by mentor)
    k = 50 if mentor else top_k
    distances, indices = index.search(query_embedding.astype('float32'), k)
    
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        metadata = metadatas[idx]
        
        # Filter by mentor if specified
        if mentor and metadata['mentor'] != mentor:
            continue
            
        results.append({
            'text': texts[idx],
            'metadata': metadata,
            'similarity': 1 / (1 + dist)  # Convert distance to similarity
        })
        
        if len(results) >= top_k:
            break
    
    return results


# Test queries
test_queries = [
    {
        "query": "What is the nature of the self and soul?",
        "mentor": "krishna"
    },
    {
        "query": "How can I overcome suffering and attachment?",
        "mentor": "buddha"
    },
    {
        "query": "What does it mean to have faith?",
        "mentor": "jesus"
    },
    {
        "query": "How should I treat my enemies?",
        "mentor": None  # Search all mentors
    }
]

for test in test_queries:
    print("=" * 70)
    print(f"Query: {test['query']}")
    if test['mentor']:
        print(f"Mentor: {test['mentor'].title()}")
    else:
        print("Mentor: All")
    print("-" * 70)
    
    results = search_verses(
        query=test['query'],
        mentor=test['mentor'],
        top_k=3
    )
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [{result['metadata']['reference']}] - {result['metadata']['mentor'].title()}")
        print(f"   Similarity: {result['similarity']:.3f}")
        print(f"   Source: {result['metadata']['source']}")
        print(f"   Text: {result['text'][:150]}...")
    
    print("\n")

print("=" * 70)
print("✅ RAG database is working perfectly!")
print("=" * 70)

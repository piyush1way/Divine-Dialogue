#!/usr/bin/env python3
"""
Divine Dialogue RAG Database Builder
Processes sacred texts and creates a vector database for semantic search.
Supports ChromaDB (primary) with FAISS fallback for SQLite compatibility.
"""

import json
import os
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Import sentence transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("ERROR: sentence-transformers not installed. Run: pip install sentence-transformers")
    exit(1)


class SacredTextsRAG:
    """RAG database builder for sacred texts"""
    
    def __init__(self, data_dir: str = "sacred-scriptures-mcp/data"):
        self.data_dir = Path(data_dir)
        self.documents = []
        self.stats = {
            "krishna": 0,
            "buddha": 0,
            "jesus": 0,
            "total": 0
        }
        self.vectorstore_type = None
        self.db_path = None
        
    def load_bhagavad_gita(self) -> List[Dict[str, Any]]:
        """Load and preprocess Bhagavad Gita verses"""
        print("📖 Loading Bhagavad Gita...")
        file_path = self.data_dir / "bhagavad_gita_verses.json"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            verses = json.load(f)
        
        documents = []
        for verse in verses:
            transliteration = verse.get("transliteration", "").strip()
            if not transliteration:
                continue
            
            doc = {
                "text": transliteration,
                "metadata": {
                    "mentor": "krishna",
                    "source": "Bhagavad Gita",
                    "reference": f"{verse['chapter_number']}.{verse['verse_number']}",
                    "chapter": verse['chapter_number'],
                    "verse": verse['verse_number']
                }
            }
            documents.append(doc)
        
        self.stats["krishna"] = len(documents)
        print(f"  ✓ Loaded {len(documents)} verses from Bhagavad Gita")
        return documents
    
    def load_dhammapada(self) -> List[Dict[str, Any]]:
        """Load and preprocess Dhammapada verses"""
        print("📖 Loading Dhammapada...")
        file_path = self.data_dir / "dhammapada.json"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = []
        for chapter in data.get("chapters", []):
            chapter_num = chapter.get("number", 0)
            for verse in chapter.get("verses", []):
                text = verse.get("english", "").strip()
                if not text:
                    continue
                
                text = re.sub(r'\s+', ' ', text)
                
                doc = {
                    "text": text,
                    "metadata": {
                        "mentor": "buddha",
                        "source": "Dhammapada",
                        "reference": f"Verse {verse['number']}",
                        "chapter": chapter_num,
                        "verse": verse['number']
                    }
                }
                documents.append(doc)
        
        self.stats["buddha"] = len(documents)
        print(f"  ✓ Loaded {len(documents)} verses from Dhammapada")
        return documents
    
    def load_bible_gospels(self) -> List[Dict[str, Any]]:
        """Load and preprocess Bible - Gospels only"""
        print("📖 Loading Bible (Gospels only)...")
        file_path = self.data_dir / "kjv_bible.json"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        gospels = ["Matthew", "Mark", "Luke", "John"]
        documents = []
        
        for book in data.get("books", []):
            book_name = book.get("name", "")
            if book_name in gospels:
                for chapter in book.get("chapters", []):
                    chapter_num = chapter.get("chapter", 0)
                    for verse in chapter.get("verses", []):
                        text = verse.get("text", "").strip()
                        if not text:
                            continue
                        
                        verse_num = verse.get("verse", 0)
                        
                        doc = {
                            "text": text,
                            "metadata": {
                                "mentor": "jesus",
                                "source": f"Gospel of {book_name}",
                                "reference": f"{book_name} {chapter_num}:{verse_num}",
                                "chapter": chapter_num,
                                "verse": verse_num,
                                "book": book_name
                            }
                        }
                        documents.append(doc)
        
        self.stats["jesus"] = len(documents)
        print(f"  ✓ Loaded {len(documents)} verses from Bible Gospels")
        return documents
    
    def preprocess_all(self) -> List[Dict[str, Any]]:
        """Load and preprocess all sacred texts"""
        print("\n🔄 Starting preprocessing of all sacred texts...\n")
        
        gita_docs = self.load_bhagavad_gita()
        dhammapada_docs = self.load_dhammapada()
        gospels_docs = self.load_bible_gospels()
        
        self.documents = gita_docs + dhammapada_docs + gospels_docs
        self.stats["total"] = len(self.documents)
        
        print(f"\n✅ Total documents preprocessed: {self.stats['total']}")
        return self.documents
    
    def save_preprocessed(self, output_path: str = "sacred_texts_preprocessed.json"):
        """Save preprocessed documents to JSON"""
        print(f"\n💾 Saving preprocessed data to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Saved {len(self.documents)} documents")

    def build_vector_database(self):
        """Build vector database with ChromaDB (primary) and FAISS (fallback)"""
        print(f"\n🔨 Building vector database...")
        
        # Try ChromaDB first
        try:
            return self._build_chromadb()
        except Exception as e:
            error_msg = str(e).lower()
            if "sqlite" in error_msg or "notsupported" in error_msg or "version" in error_msg:
                print(f"\n⚠️  ChromaDB failed due to SQLite version conflict.")
                print(f"    Error: {str(e)[:100]}")
                print(f"    Falling back to FAISS...")
                return self._build_faiss()
            else:
                print(f"\n⚠️  ChromaDB failed with error: {str(e)[:100]}")
                print(f"    Falling back to FAISS...")
                return self._build_faiss()
    
    def _build_chromadb(self):
        """Build ChromaDB vector database"""
        print(f"  Attempting ChromaDB setup...")
        
        import chromadb
        from chromadb.utils import embedding_functions
        
        db_path = "sacred_texts_rag"
        client = chromadb.PersistentClient(path=db_path)
        
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        collection_name = "sacred_texts"
        try:
            client.delete_collection(name=collection_name)
        except:
            pass
        
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            metadata={"description": "Sacred texts for Divine Dialogue mentors"}
        )
        
        texts = [doc["text"] for doc in self.documents]
        metadatas = [doc["metadata"] for doc in self.documents]
        ids = [f"{doc['metadata']['mentor']}_{i}" for i, doc in enumerate(self.documents)]
        
        batch_size = 100
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        print(f"  📦 Adding {len(texts)} documents in {total_batches} batches...")
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            collection.add(
                documents=batch_texts,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            
            batch_num = (i // batch_size) + 1
            print(f"    ✓ Batch {batch_num}/{total_batches} added")
        
        print(f"\n✅ ChromaDB setup successful!")
        print(f"  📊 Collection: {collection_name}")
        print(f"  📍 Location: {db_path}")
        print(f"  📝 Total vectors: {collection.count()}")
        
        self.vectorstore_type = "chromadb"
        self.db_path = db_path
        return ("chromadb", client, collection)
    
    def _build_faiss(self):
        """Build FAISS vector database as fallback"""
        print(f"  Setting up FAISS vector store...")
        
        # Install FAISS if not available
        try:
            import faiss
        except ImportError:
            print("  📦 Installing faiss-cpu...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu", "-q"])
            import faiss
        
        import numpy as np
        
        db_path = "sacred_texts_rag_faiss"
        
        print("  🤖 Loading embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        texts = [doc["text"] for doc in self.documents]
        metadatas = [doc["metadata"] for doc in self.documents]
        
        print(f"  🔢 Generating embeddings for {len(texts)} documents...")
        embeddings = model.encode(texts, show_progress_bar=True, batch_size=32, convert_to_numpy=True)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype('float32'))
        
        os.makedirs(db_path, exist_ok=True)
        faiss.write_index(index, os.path.join(db_path, "index.faiss"))
        
        with open(os.path.join(db_path, "texts.json"), 'w', encoding='utf-8') as f:
            json.dump(texts, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(db_path, "metadatas.json"), 'w', encoding='utf-8') as f:
            json.dump(metadatas, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ FAISS fallback successful!")
        print(f"  📍 Location: {db_path}")
        print(f"  📝 Total vectors: {index.ntotal}")
        
        self.vectorstore_type = "faiss"
        self.db_path = db_path
        return ("faiss", {"index": index, "texts": texts, "metadatas": metadatas, "model": model})
    
    def test_semantic_search(self, vectorstore_type: str, vectorstore: Any):
        """Test semantic search with sample queries"""
        print("\n🔍 Testing semantic search...\n")
        
        test_queries = [
            {
                "query": "How do I find inner peace and calm my mind?",
                "mentor": "buddha",
                "description": "Buddha - Inner Peace"
            },
            {
                "query": "What is my duty and purpose in life?",
                "mentor": "krishna",
                "description": "Krishna - Duty & Purpose"
            },
            {
                "query": "How should I love and forgive others?",
                "mentor": "jesus",
                "description": "Jesus - Love & Forgiveness"
            }
        ]
        
        results_summary = []
        
        for test in test_queries:
            print(f"📌 Query: {test['query']}")
            print(f"   Target Mentor: {test['mentor']}")
            
            if vectorstore_type == "chromadb":
                results = vectorstore.query(
                    query_texts=[test['query']],
                    n_results=3,
                    where={"mentor": test['mentor']}
                )
                
                print(f"   Results:")
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ), 1):
                    similarity = 1 - distance
                    print(f"     {i}. [{metadata['reference']}] (similarity: {similarity:.3f})")
                    print(f"        {doc[:100]}...")
                
                results_summary.append({
                    "query": test['query'],
                    "mentor": test['mentor'],
                    "top_result": results['metadatas'][0][0]['reference'],
                    "similarity": 1 - results['distances'][0][0]
                })
                
            else:  # FAISS
                import numpy as np
                
                query_embedding = vectorstore["model"].encode([test['query']], convert_to_numpy=True)
                
                k = 50
                distances, indices = vectorstore["index"].search(query_embedding.astype('float32'), k)
                
                filtered_results = []
                for idx, dist in zip(indices[0], distances[0]):
                    if vectorstore["metadatas"][idx]["mentor"] == test['mentor']:
                        filtered_results.append({
                            "text": vectorstore["texts"][idx],
                            "metadata": vectorstore["metadatas"][idx],
                            "distance": dist
                        })
                        if len(filtered_results) >= 3:
                            break
                
                print(f"   Results:")
                for i, result in enumerate(filtered_results, 1):
                    similarity = 1 / (1 + result['distance'])
                    print(f"     {i}. [{result['metadata']['reference']}] (similarity: {similarity:.3f})")
                    print(f"        {result['text'][:100]}...")
                
                if filtered_results:
                    results_summary.append({
                        "query": test['query'],
                        "mentor": test['mentor'],
                        "top_result": filtered_results[0]['metadata']['reference'],
                        "similarity": 1 / (1 + filtered_results[0]['distance'])
                    })
            
            print()
        
        return results_summary

    def print_analysis_report(self, results_summary: List[Dict]):
        """Print comprehensive analysis report"""
        print("\n" + "="*70)
        print("📊 DIVINE DIALOGUE RAG DATABASE - ANALYSIS REPORT")
        print("="*70)
        
        print(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🗄️  Vector Store Used: {self.vectorstore_type.upper()}")
        
        print("\n📚 CORPUS STATISTICS:")
        print(f"  • Krishna (Bhagavad Gita):  {self.stats['krishna']:>5} verses")
        print(f"  • Buddha (Dhammapada):      {self.stats['buddha']:>5} verses")
        print(f"  • Jesus (Gospels):          {self.stats['jesus']:>5} verses")
        print(f"  {'─' * 40}")
        print(f"  • TOTAL:                    {self.stats['total']:>5} verses")
        
        print("\n🎯 SEMANTIC SEARCH TEST RESULTS:")
        for result in results_summary:
            print(f"\n  Query: \"{result['query']}\"")
            print(f"  Mentor: {result['mentor'].title()}")
            print(f"  Top Match: {result['top_result']}")
            print(f"  Similarity: {result['similarity']:.3f}")
        
        print("\n💾 OUTPUT FILES:")
        print(f"  • Vector Database: ./{self.db_path}/")
        print(f"  • Preprocessed JSON: ./sacred_texts_preprocessed.json")
        
        print("\n✅ RAG DATABASE READY FOR PRODUCTION")
        print("="*70)
        
        # Save report to file
        report_path = "rag_analysis_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("DIVINE DIALOGUE RAG DATABASE - ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Vector Store Used: {self.vectorstore_type.upper()}\n")
            f.write(f"Database Location: ./{self.db_path}/\n\n")
            f.write("CORPUS STATISTICS:\n")
            f.write(f"  Krishna (Bhagavad Gita):  {self.stats['krishna']:>5} verses\n")
            f.write(f"  Buddha (Dhammapada):      {self.stats['buddha']:>5} verses\n")
            f.write(f"  Jesus (Gospels):          {self.stats['jesus']:>5} verses\n")
            f.write(f"  {'─' * 40}\n")
            f.write(f"  TOTAL:                    {self.stats['total']:>5} verses\n\n")
            f.write("SEMANTIC SEARCH TEST RESULTS:\n")
            for result in results_summary:
                f.write(f"\n  Query: \"{result['query']}\"\n")
                f.write(f"  Mentor: {result['mentor'].title()}\n")
                f.write(f"  Top Match: {result['top_result']}\n")
                f.write(f"  Similarity: {result['similarity']:.3f}\n")
            f.write("\n" + "="*70 + "\n")
        
        print(f"  • Analysis Report: ./{report_path}")
        print()
    
    def print_final_instructions(self):
        """Print final usage instructions"""
        print("-" * 70)
        print("✅ RAG DATABASE SETUP COMPLETE!")
        print("-" * 70)
        print(f"Vector Store Used: {self.vectorstore_type.upper()}")
        print(f"Database Location: ./{self.db_path}")
        print(f"Total Documents: {self.stats['total']:,}")
        print()
        print("NEXT STEP:")
        print("You can now use this vector store in your LangGraph application.")
        print()
        
        if self.vectorstore_type == "chromadb":
            print("Load it using:")
            print("  import chromadb")
            print("  from chromadb.utils import embedding_functions")
            print()
            print(f"  client = chromadb.PersistentClient(path='{self.db_path}')")
            print("  embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(")
            print("      model_name='sentence-transformers/all-MiniLM-L6-v2'")
            print("  )")
            print("  collection = client.get_collection(")
            print("      name='sacred_texts',")
            print("      embedding_function=embedding_fn")
            print("  )")
        else:  # FAISS
            print("Load it using:")
            print("  import faiss")
            print("  import json")
            print("  from sentence_transformers import SentenceTransformer")
            print()
            print(f"  index = faiss.read_index('{self.db_path}/index.faiss')")
            print(f"  with open('{self.db_path}/texts.json', 'r') as f:")
            print("      texts = json.load(f)")
            print(f"  with open('{self.db_path}/metadatas.json', 'r') as f:")
            print("      metadatas = json.load(f)")
            print("  model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')")
        
        print("-" * 70)
        print()


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("🕉️  DIVINE DIALOGUE RAG DATABASE BUILDER")
    print("="*70)
    
    # Initialize RAG builder
    rag = SacredTextsRAG()
    
    # Step 1: Preprocess all texts
    rag.preprocess_all()
    
    # Step 2: Save preprocessed data
    rag.save_preprocessed()
    
    # Step 3: Build vector database (ChromaDB with FAISS fallback)
    vectorstore_type, *vectorstore_components = rag.build_vector_database()
    
    if vectorstore_type == "chromadb":
        client, collection = vectorstore_components
        vectorstore = collection
    else:  # FAISS
        vectorstore = vectorstore_components[0]
    
    # Step 4: Test semantic search
    results = rag.test_semantic_search(vectorstore_type, vectorstore)
    
    # Step 5: Print analysis report
    rag.print_analysis_report(results)
    
    # Step 6: Print final instructions
    rag.print_final_instructions()


if __name__ == "__main__":
    main()

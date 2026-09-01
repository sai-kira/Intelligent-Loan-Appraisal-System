import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import psycopg
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sentence_transformers import CrossEncoder

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/CentralBankDB")

class PolicyRetriever:
    def __init__(self):
        # Initialize the dense embedder
        self.embedder = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
        
        # Initialize the cross-encoder for Late-Interaction Re-ranking
        # This model is very fast on CPU and highly precise for QA matching
        print("Loading Cross-Encoder model...")
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        print("Cross-Encoder loaded successfully.")

    def reciprocal_rank_fusion(self, dense_results, sparse_results, k=60):
        """
        Fuses two ranked lists using Reciprocal Rank Fusion (RRF).
        RRF_score = 1 / (k + rank)
        """
        fused_scores = {}
        
        # Helper to process a result list
        def add_to_fusion(results):
            for rank, row in enumerate(results):
                doc_id = row['id']
                if doc_id not in fused_scores:
                    fused_scores[doc_id] = {'score': 0, 'data': row}
                fused_scores[doc_id]['score'] += 1 / (k + rank + 1)

        add_to_fusion(dense_results)
        add_to_fusion(sparse_results)
        
        # Sort by fused score descending
        fused_list = sorted(fused_scores.values(), key=lambda x: x['score'], reverse=True)
        return [item['data'] for item in fused_list]

    def retrieve(self, query: str, top_k: int = 3):
        """
        The full GAHR-MSR Pipeline:
        1. Embed query
        2. Run Vector Search (Dense)
        3. Run BM25 Search (Sparse)
        4. Fuse with RRF
        5. Re-rank with Cross-Encoder
        """
        query_embedding = self.embedder.embed_query(query)
        
        dense_results = []
        sparse_results = []
        
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                # 1. DENSE SEARCH (Vector Cosine Similarity)
                cur.execute("""
                    SELECT id, content, metadata
                    FROM policy_documents
                    ORDER BY embedding <=> %s::vector
                    LIMIT 20
                """, (query_embedding,))
                
                columns = [desc[0] for desc in cur.description]
                for row in cur.fetchall():
                    dense_results.append(dict(zip(columns, row)))
                    
                # 2. SPARSE SEARCH (BM25 Lexical Search)
                # We use plainto_tsquery to handle natural language questions
                cur.execute("""
                    SELECT id, content, metadata
                    FROM policy_documents
                    WHERE fts @@ plainto_tsquery('english', %s)
                    ORDER BY ts_rank(fts, plainto_tsquery('english', %s)) DESC
                    LIMIT 20
                """, (query, query))
                
                columns = [desc[0] for desc in cur.description]
                for row in cur.fetchall():
                    sparse_results.append(dict(zip(columns, row)))

        # 3. RECIPROCAL RANK FUSION
        fused_results = self.reciprocal_rank_fusion(dense_results, sparse_results)
        
        # Take the top N from fusion for heavy re-ranking
        candidates = fused_results[:10]
        
        if not candidates:
            return []

        # 4. CROSS-ENCODER RE-RANKING
        # Create pairs of (query, document) to score
        pairs = [[query, doc['content']] for doc in candidates]
        scores = self.cross_encoder.predict(pairs)
        
        # Attach scores and sort
        for doc, score in zip(candidates, scores):
            doc['rerank_score'] = float(score)
            
        reranked = sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
        
        # Return top_k with formatted citations
        final_results = []
        for doc in reranked[:top_k]:
            meta = doc['metadata']
            doc_name = meta.get('document_name', 'Unknown Document')
            chunk_idx = meta.get('chunk_index', 'N/A')
            
            # Format the citation string specifically for the LLM context
            citation = f"[Doc: {doc_name}, Chunk: {chunk_idx}]"
            final_results.append(f"{citation}\n{doc['content']}")
            
        return final_results

# Simple manual test when running this script
if __name__ == "__main__":
    print("Testing the GAHR-MSR RAG Pipeline...")
    retriever = PolicyRetriever()
    
    test_query = "What is the maximum LTV for a home loan of 50 lakhs?"
    print(f"\\nQuery: {test_query}")
    print("-" * 50)
    
    results = retriever.retrieve(test_query, top_k=2)
    for i, res in enumerate(results):
        print(f"\\nRESULT {i+1}:\\n{res}\\n")

import os
import psycopg
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DB_URL = "postgresql://postgres:1424@localhost:5432/CentralBankDB"

def setup_database():
    """Create the hybrid search table if it doesn't exist."""
    print("Setting up database schema...")
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE EXTENSION IF NOT EXISTS vector;
                DROP TABLE IF EXISTS policy_documents CASCADE;
                CREATE TABLE policy_documents (
                    id serial PRIMARY KEY,
                    content text NOT NULL,
                    metadata jsonb NOT NULL,
                    embedding vector(3072),
                    fts tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
                );
                
                -- Create index for fast keyword search (Exact vector search will be used for dense)
                CREATE INDEX IF NOT EXISTS policy_fts_idx ON policy_documents USING gin (fts);
            """)
        conn.commit()
    print("Database schema ready.")

import re

def clean_text(text: str) -> str:
    """Remove HTML tags and citation markers."""
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'【.*?】|\[.*?\]', '', text)  # Remove citation markers
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

def semantic_chunk_text(text: str, chunk_size: int = 1000):
    """Chunk text by sentences to prevent breaking."""
    text = clean_text(text)
    # Split by periods followed by space
    sentences = re.split(r'(?<=\.)\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def ingest_document(file_path: str, doc_name: str, embeddings_model):
    """Read a document, chunk it, embed it, and store in PostgreSQL."""
    print(f"Ingesting {doc_name}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    chunks = semantic_chunk_text(content)
    print(f"Split {doc_name} into {len(chunks)} chunks. Generating embeddings...")
    
    # Generate all embeddings in a batch
    embeddings = embeddings_model.embed_documents(chunks)
    
    # Insert into database
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                metadata = {
                    "document_name": doc_name,
                    "chunk_index": i
                }
                import json
                cur.execute("""
                    INSERT INTO policy_documents (content, metadata, embedding)
                    VALUES (%s, %s, %s)
                """, (chunk, json.dumps(metadata), emb))
        conn.commit()
    print(f"Successfully inserted {len(chunks)} chunks into the database.")

def main():
    from dotenv import load_dotenv
    # Go up one directory to find backend/.env
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY environment variable is missing.")
        print("Please set it in your terminal or .env file before running this script.")
        return

    setup_database()
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    # Paths to our core documents (update paths if needed)
    base_dir = r"C:\Users\Karma\.gemini\antigravity\worktrees\Intelligent-Loan-Appraisal-System\build-ai-loan-appraisal"
    files_to_ingest = {
        "GR3_Appraisal_Metrics": os.path.join(base_dir, "extracted_GR3_Loan Appraisal Metrics Analysis.docx.txt"),
        "CR3_Appraisal_Formulas": os.path.join(base_dir, "extracted_CR3_Loan Appraisal & Credit Risk Metrics_ Definitions, Formulas, and Usage.docx.txt"),
        "RBI_Retail_Guidelines": os.path.join(base_dir, "backend", "rag", "RBI_Master_Circular_Retail_Loans.txt"),
        "CBoI_Appraisal_Guidelines": os.path.join(base_dir, "backend", "rag", "CBoI_Appraisal_Guidelines.txt"),
        "ROI_Retail_MSME_Guidelines": os.path.join(base_dir, "backend", "rag", "ROI_Retail_MSME.txt"),
        "CBoI_MSE_Scoring_Models": os.path.join(base_dir, "backend", "rag", "CBoI_MSE_Scoring_Models.txt")
    }
    
    for doc_name, path in files_to_ingest.items():
        ingest_document(path, doc_name, embeddings)
        
    print("Ingestion complete! The database now has semantic vectors and BM25 search indexes.")

if __name__ == "__main__":
    main()

import psycopg
from psycopg import sql

db_url = "postgresql://postgres:1424@localhost:5432/CentralBankDB"

def test_db():
    try:
        # First, connect to default postgres DB to create the CentralBankDB if it doesn't exist
        print("Testing connection...")
        conn = psycopg.connect("postgresql://postgres:1424@localhost:5432/postgres")
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if CentralBankDB exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'CentralBankDB'")
        exists = cur.fetchone()
        if not exists:
            print("Database CentralBankDB does not exist. Creating it...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("CentralBankDB")))
        else:
            print("Database CentralBankDB already exists.")
            
        cur.close()
        conn.close()
        
        # Now connect to CentralBankDB and enable pgvector
        conn = psycopg.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("Extension 'vector' is ready.")
        
        # Test table creation
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test_vector (
                id serial PRIMARY KEY,
                embedding vector(3)
            );
        """)
        print("Successfully created a test vector table.")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_db()

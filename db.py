import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection pool for better performance
db_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=os.getenv('DB_NAME', 'Niyati_Engine'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'gokul2005'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432')
)

def get_connection():
    """Get a connection from the pool"""
    try:
        return db_pool.getconn()
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def release_connection(conn):
    """Release a connection back to the pool"""
    try:
        if conn:
            db_pool.putconn(conn)
    except Exception as e:
        print(f"Error releasing connection: {e}")

def release_all_connections():
    """Release all connections and close the pool"""
    try:
        db_pool.closeall()
    except Exception as e:
        print(f"Error closing connection pool: {e}")

def init_db():
    """Initialize database tables if they don't exist"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create tables manually (more reliable than reading file)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                company VARCHAR(200),
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(150) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                job_description TEXT NOT NULL,
                cutoff_score DECIMAL(5, 2) NOT NULL,
                total_candidates INTEGER DEFAULT 0,
                accepted_count INTEGER DEFAULT 0,
                rejected_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                session_id INTEGER REFERENCES analysis_sessions(id) ON DELETE CASCADE,
                name VARCHAR(200) NOT NULL,
                role VARCHAR(100),
                similarity DECIMAL(5, 2) DEFAULT 0,
                skill DECIMAL(5, 2) DEFAULT 0,
                experience DECIMAL(5, 2) DEFAULT 0,
                final_score DECIMAL(5, 2) DEFAULT 0,
                matched_skills TEXT[],
                missing_skills TEXT[],
                job_description TEXT,
                cutoff_score DECIMAL(5, 2),
                status VARCHAR(20) CHECK (status IN ('accepted', 'rejected')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_user_id ON candidates(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_session_id ON candidates(session_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_final_score ON candidates(final_score DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_created_at ON candidates(created_at DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analysis_sessions_user_id ON analysis_sessions(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analysis_sessions_created_at ON analysis_sessions(created_at DESC);")
        
        conn.commit()
        cursor.close()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            release_connection(conn)
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---------------- DATABASE POOL ----------------
db_pool = None

def init_pool():
    global db_pool

    if db_pool is None:
        DATABASE_URL = os.getenv("DATABASE_URL")

        if DATABASE_URL:
            # Use DATABASE_URL if available
            db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=DATABASE_URL
            )
        else:
            # Use individual database parameters
            db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dbname=os.getenv("DB_NAME", "Niyati_Engine"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", ""),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432")
            )

        print("✅ Database pool initialized")


# ---------------- GET CONNECTION ----------------
def get_connection():
    try:
        init_pool()
        return db_pool.getconn()
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")
        raise


# ---------------- RELEASE CONNECTION ----------------
def release_connection(conn):
    try:
        if conn and db_pool:
            db_pool.putconn(conn)
    except Exception as e:
        print(f"❌ Error releasing connection: {e}")


# ---------------- CLOSE ALL ----------------
def release_all_connections():
    global db_pool
    if db_pool:
        db_pool.closeall()
        print("🔒 All DB connections closed")


# ---------------- INIT DATABASE ----------------
def init_db():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # USERS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(150) UNIQUE,
                company VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)

        # CANDIDATES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                name VARCHAR(200),
                role VARCHAR(100),
                similarity FLOAT,
                skill FLOAT,
                experience FLOAT,
                final_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cursor.close()

        print("✅ Database initialized successfully")

    except Exception as e:
        print(f"❌ DB Init Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            release_connection(conn)

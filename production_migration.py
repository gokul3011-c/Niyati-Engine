"""
Production Migration Script
Run this on your deployed database to add missing columns
Usage: python production_migration.py
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Get database connection"""
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        return psycopg2.connect(database_url)
    else:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME", "Niyati_Engine"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )

def run_migration():
    """Add all missing columns to users table"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("🔍 Checking for missing columns in users table...")
        
        # List of columns to check and add
        columns_to_add = [
            ('company', 'VARCHAR(200)'),
            ('email', 'VARCHAR(150)'),
            ('last_login', 'TIMESTAMP'),
            ('is_active', 'BOOLEAN DEFAULT TRUE')
        ]
        
        for col_name, col_type in columns_to_add:
            # Check if column exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = %s
            """, (col_name,))
            
            if cursor.fetchone():
                print(f"✅ Column '{col_name}' already exists")
            else:
                # Add the missing column
                cursor.execute(f"""
                    ALTER TABLE users 
                    ADD COLUMN {col_name} {col_type}
                """)
                conn.commit()
                print(f"✅ Added column '{col_name}' ({col_type})")
        
        # Also check if candidates table needs session_id column
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'candidates' AND column_name = 'session_id'
        """)
        
        if not cursor.fetchone():
            cursor.execute("""
                ALTER TABLE candidates 
                ADD COLUMN session_id INTEGER REFERENCES analysis_sessions(id)
            """)
            conn.commit()
            print("✅ Added column 'session_id' to candidates table")
        else:
            print("✅ Column 'session_id' already exists in candidates table")
        
        # Check for other missing columns in candidates
        candidate_columns = [
            ('matched_skills', 'TEXT[]'),
            ('missing_skills', 'TEXT[]'),
            ('job_description', 'TEXT'),
            ('cutoff_score', 'DECIMAL(5, 2)'),
            ('status', 'VARCHAR(20)')
        ]
        
        for col_name, col_type in candidate_columns:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'candidates' AND column_name = %s
            """, (col_name,))
            
            if not cursor.fetchone():
                cursor.execute(f"""
                    ALTER TABLE candidates 
                    ADD COLUMN {col_name} {col_type}
                """)
                conn.commit()
                print(f"✅ Added column '{col_name}' to candidates table")
        
        cursor.close()
        print("\n✅ Migration completed successfully!")
        print("🎉 All missing columns have been added!")
        
    except Exception as e:
        print(f"❌ Migration Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("🔒 Database connection closed")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Niyati Engine - Production Database Migration")
    print("=" * 60)
    run_migration()

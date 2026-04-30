from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from core_logic import process_resumes
from db import get_connection, release_connection, init_db
import pandas as pd
import bcrypt
import os
from datetime import datetime

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'niyati-secret-key-2024')

# Serve frontend files
@app.route('/')
def serve_auth():
    return send_from_directory('frontend', 'auth.html')

@app.route('/index.html')
def serve_index():
    return send_from_directory('frontend', 'index.html')

# Initialize database on startup
with app.app_context():
    try:
        init_db()
        print("✅ Database initialized")
        
        # Run comprehensive migration on startup
        print("🔍 Running database migration...")
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Create analysis_sessions table if not exists
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
            conn.commit()
            print("✅ analysis_sessions table ready")
            
            # Add missing columns to users table
            user_columns = [
                ('company', 'VARCHAR(200)'),
                ('email', 'VARCHAR(150)'),
                ('last_login', 'TIMESTAMP'),
                ('is_active', 'BOOLEAN DEFAULT TRUE')
            ]
            
            for col_name, col_type in user_columns:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = %s
                """, (col_name,))
                
                if not cursor.fetchone():
                    cursor.execute(f"""
                        ALTER TABLE users 
                        ADD COLUMN {col_name} {col_type}
                    """)
                    conn.commit()
                    print(f"✅ Added '{col_name}' to users table")
            
            # Add missing columns to candidates table
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
                print("✅ Added 'session_id' to candidates table")
            
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
                    print(f"✅ Added '{col_name}' to candidates table")
            
            cursor.close()
            release_connection(conn)
            print("✅ Database migration completed!")
            
        except Exception as e:
            print(f"⚠️  Migration error: {e}")
            if conn:
                conn.rollback()
                release_connection(conn)
                
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")

# ------------------- ANALYZE API -------------------
@app.route('/api/analyze', methods=['POST'])
def analyze_resumes():
    conn = None
    try:
        # 🔐 Get user_id (from frontend)
        user_id = request.form.get("user_id")

        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        # Get inputs
        jd = request.form.get('job_description', '')
        cutoff = float(request.form.get('cutoff', 70))

        # Validate files
        if 'resumes' not in request.files:
            return jsonify({'error': 'No resumes uploaded'}), 400

        files = request.files.getlist('resumes')

        if not jd.strip():
            return jsonify({'error': 'Job description is required'}), 400

        valid_files = [f for f in files if f.filename and f.filename.strip()]

        if len(valid_files) == 0:
            return jsonify({'error': 'Please upload valid resume files'}), 400

        # 🔥 Process resumes
        results = process_resumes(valid_files, jd)

        # Sort results
        results = sorted(results, key=lambda x: x["Final Score %"], reverse=True)

        # Separate accepted/rejected
        accepted = [r for r in results if r["Final Score %"] >= cutoff]
        rejected = [r for r in results if r["Final Score %"] < cutoff]

        # 🔥 CONNECT TO DATABASE
        conn = get_connection()
        cursor = conn.cursor()

        # 🔥 Create analysis session
        cursor.execute("""
            INSERT INTO analysis_sessions 
            (user_id, job_description, cutoff_score, total_candidates, accepted_count, rejected_count)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            int(user_id),
            jd,
            cutoff,
            len(results),
            len(accepted),
            len(rejected)
        ))
        session_id = cursor.fetchone()[0]

        # 🔥 INSERT DATA INTO DB
        for r in results:
            status = 'accepted' if r["Final Score %"] >= cutoff else 'rejected'
            
            cursor.execute("""
                INSERT INTO candidates
                (user_id, session_id, name, role, similarity, skill, experience, final_score, 
                 matched_skills, missing_skills, job_description, cutoff_score, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(user_id),
                session_id,
                str(r.get("Candidate Name")),
                str(r.get("Predicted Role")),
                float(r.get("Similarity %", 0)),
                float(r.get("Skill Match %", 0)),
                float(r.get("Experience %", 0)) if r.get("Experience %") is not None else 0,
                float(r.get("Final Score %", 0)),
                r.get("Matched Skills", []),
                r.get("Missing Skills", []),
                jd,
                cutoff,
                status
            ))

        conn.commit()
        cursor.close()
        release_connection(conn)

        # 🔥 Return response
        return jsonify({
            'total': len(results),
            'accepted': len(accepted),
            'rejected': len(rejected),
            'session_id': session_id,
            'accepted_candidates': accepted,
            'rejected_candidates': rejected,
            'all_candidates': results
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()
            release_connection(conn)
        return jsonify({'error': str(e)}), 500


# ------------------- SIGNUP -------------------
@app.route('/api/signup', methods=['POST'])
def signup():
    conn = None
    try:
        data = request.json
        company = data.get("company", "")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email", "")

        print(f"📝 Signup attempt - Username: {username}, Email: {email}, Company: {company}")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            cursor.close()
            release_connection(conn)
            print(f"⚠️  Username already exists: {username}")
            return jsonify({"error": "Username already exists"}), 409

        print(f"✅ Inserting new user into database...")
        cursor.execute(
            "INSERT INTO users (company, username, password, email) VALUES (%s, %s, %s, %s) RETURNING id",
            (company if company else None, username, hashed_password, email if email else None)
        )

        user_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ User created successfully! ID: {user_id}, Username: {username}")
        
        cursor.close()
        release_connection(conn)

        return jsonify({
            "message": "Signup successful",
            "user_id": user_id,
            "username": username,
            "company": company
        }), 201

    except Exception as e:
        print(f"❌ Signup Error: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
            release_connection(conn)
        return jsonify({"error": str(e)}), 500



# ------------------- LOGIN -------------------
@app.route('/api/login', methods=['POST'])
def login():
    conn = None
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        print(f"🔐 Login attempt - Username: {username}")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, password FROM users WHERE username=%s AND is_active=TRUE",
            (username,)
        )

        user = cursor.fetchone()

        if user:
            user_id, stored_password = user
            print(f"✅ User found in database - ID: {user_id}")
            
            # Verify password (supports both hashed and plain text for backward compatibility)
            password_valid = False
            if stored_password.startswith('$2b$') or stored_password.startswith('$2a$'):
                # Bcrypt hashed password
                password_valid = bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
            else:
                # Plain text password (legacy)
                password_valid = (password == stored_password)
            
            if password_valid:
                # Update last login
                cursor.execute(
                    "UPDATE users SET last_login=%s WHERE id=%s",
                    (datetime.now(), user_id)
                )
                conn.commit()
                
                # Fetch full user data
                cursor.execute(
                    "SELECT username, company, email FROM users WHERE id=%s",
                    (user_id,)
                )
                user_data = cursor.fetchone()
                
                print(f"✅ Login successful for user: {username}")
                
                cursor.close()
                release_connection(conn)
                
                return jsonify({
                    "message": "Login successful",
                    "user_id": user_id,
                    "username": user_data[0],
                    "company": user_data[1] or "",
                    "email": user_data[2] or ""
                }), 200
            else:
                print(f"❌ Invalid password for user: {username}")
                cursor.close()
                release_connection(conn)
                return jsonify({"error": "Invalid credentials"}), 401
        else:
            print(f"❌ User not found in database: {username}")
            cursor.close()
            release_connection(conn)
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print(f"❌ Login Error: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
            release_connection(conn)
        return jsonify({"error": str(e)}), 500


# ------------------- DOWNLOAD CSV -------------------
@app.route('/api/download', methods=['POST'])
def download_results():
    try:
        data = request.json
        results = data.get('results', [])

        df = pd.DataFrame(results)
        csv_data = df.to_csv(index=False)

        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=niyati_results.csv'
        }

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ------------------- GET USER HISTORY -------------------
@app.route('/api/user/<int:user_id>/history', methods=['GET'])
def get_user_history(user_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get all analysis sessions for this user
        cursor.execute("""
            SELECT id, job_description, cutoff_score, total_candidates, 
                   accepted_count, rejected_count, created_at
            FROM analysis_sessions
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))

        sessions = cursor.fetchall()
        sessions_list = []

        for session in sessions:
            sessions_list.append({
                'session_id': session[0],
                'job_description': session[1][:100] + '...' if len(session[1]) > 100 else session[1],
                'cutoff_score': float(session[2]),
                'total_candidates': session[3],
                'accepted_count': session[4],
                'rejected_count': session[5],
                'created_at': session[6].isoformat()
            })

        cursor.close()
        release_connection(conn)

        return jsonify({
            'user_id': user_id,
            'total_sessions': len(sessions_list),
            'sessions': sessions_list
        }), 200

    except Exception as e:
        if conn:
            release_connection(conn)
        return jsonify({'error': str(e)}), 500


# ------------------- GET SESSION DETAILS -------------------
@app.route('/api/session/<int:session_id>', methods=['GET'])
def get_session_details(session_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get session info
        cursor.execute("""
            SELECT id, user_id, job_description, cutoff_score, 
                   total_candidates, accepted_count, rejected_count, created_at
            FROM analysis_sessions
            WHERE id = %s
        """, (session_id,))

        session = cursor.fetchone()

        if not session:
            cursor.close()
            release_connection(conn)
            return jsonify({'error': 'Session not found'}), 404

        # Get candidates for this session
        cursor.execute("""
            SELECT id, name, role, similarity, skill, experience, 
                   final_score, matched_skills, missing_skills, status
            FROM candidates
            WHERE session_id = %s
            ORDER BY final_score DESC
        """, (session_id,))

        candidates = cursor.fetchall()
        candidates_list = []

        for candidate in candidates:
            candidates_list.append({
                'id': candidate[0],
                'name': candidate[1],
                'role': candidate[2],
                'similarity': float(candidate[3]),
                'skill_match': float(candidate[4]),
                'experience': float(candidate[5]) if candidate[5] else 0,
                'final_score': float(candidate[6]),
                'matched_skills': candidate[7],
                'missing_skills': candidate[8],
                'status': candidate[9]
            })

        cursor.close()
        release_connection(conn)

        return jsonify({
            'session_id': session[0],
            'user_id': session[1],
            'job_description': session[2],
            'cutoff_score': float(session[3]),
            'total_candidates': session[4],
            'accepted_count': session[5],
            'rejected_count': session[6],
            'created_at': session[7].isoformat(),
            'candidates': candidates_list
        }), 200

    except Exception as e:
        if conn:
            release_connection(conn)
        return jsonify({'error': str(e)}), 500


# ------------------- GET USER PROFILE -------------------
@app.route('/api/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, company, username, email, created_at, last_login
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            cursor.close()
            release_connection(conn)
            return jsonify({'error': 'User not found'}), 404

        # Get user stats
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT a.id) as total_sessions,
                COUNT(DISTINCT c.id) as total_candidates,
                COUNT(CASE WHEN c.status = 'accepted' THEN 1 END) as total_accepted,
                COUNT(CASE WHEN c.status = 'rejected' THEN 1 END) as total_rejected,
                COALESCE(AVG(c.final_score), 0) as avg_score
            FROM analysis_sessions a
            LEFT JOIN candidates c ON a.user_id = c.user_id 
                AND c.created_at >= a.created_at
            WHERE a.user_id = %s
        """, (user_id,))

        stats = cursor.fetchone()

        cursor.close()
        release_connection(conn)

        return jsonify({
            'user_id': user[0],
            'company': user[1],
            'username': user[2],
            'email': user[3],
            'member_since': user[4].isoformat(),
            'last_login': user[5].isoformat() if user[5] else None,
            'stats': {
                'total_sessions': stats[0],
                'total_candidates_analyzed': stats[1],
                'total_accepted': stats[2],
                'total_rejected': stats[3],
                'average_score': round(float(stats[4]), 2)
            }
        }), 200

    except Exception as e:
        if conn:
            release_connection(conn)
        return jsonify({'error': str(e)}), 500


# ------------------- UPDATE USER PROFILE -------------------
@app.route('/api/user/<int:user_id>/profile', methods=['PUT'])
def update_user_profile(user_id):
    conn = None
    try:
        data = request.json
        username = data.get('username')
        company = data.get('company', '')
        email = data.get('email', '')

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        conn = get_connection()
        cursor = conn.cursor()

        # Check if username already exists for another user
        cursor.execute(
            "SELECT id FROM users WHERE username=%s AND id != %s",
            (username, user_id)
        )
        if cursor.fetchone():
            cursor.close()
            release_connection(conn)
            return jsonify({'error': 'Username already exists'}), 409

        # Update user profile
        cursor.execute("""
            UPDATE users 
            SET username=%s, company=%s, email=%s
            WHERE id=%s
            RETURNING id, username, company, email
        """, (username, company if company else None, email if email else None, user_id))

        updated_user = cursor.fetchone()
        conn.commit()
        cursor.close()
        release_connection(conn)

        return jsonify({
            'message': 'Profile updated successfully',
            'user_id': updated_user[0],
            'username': updated_user[1],
            'company': updated_user[2] or '',
            'email': updated_user[3] or ''
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()
            release_connection(conn)
        return jsonify({'error': str(e)}), 500


# ------------------- DELETE SCREENINGS -------------------
@app.route('/api/screenings/delete', methods=['POST'])
def delete_screenings():
    conn = None
    try:
        data = request.json
        user_id = data.get('user_id')
        session_ids = data.get('session_ids', [])
        
        if not user_id or not session_ids:
            return jsonify({'error': 'User ID and session IDs are required'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Delete candidates for these sessions
        for session_id in session_ids:
            cursor.execute("""
                DELETE FROM candidates
                WHERE user_id = %s AND id IN (
                    SELECT id FROM candidates 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC
                    LIMIT (SELECT total_candidates FROM analysis_sessions WHERE id = %s)
                )
            """, (user_id, user_id, session_id))
            
            # Delete the session
            cursor.execute("""
                DELETE FROM analysis_sessions
                WHERE id = %s AND user_id = %s
            """, (session_id, user_id))
        
        conn.commit()
        cursor.close()
        release_connection(conn)
        
        return jsonify({
            'message': f'Successfully deleted {len(session_ids)} screening(s)',
            'deleted_count': len(session_ids)
        }), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
            release_connection(conn)
        return jsonify({'error': str(e)}), 500


# ------------------- RUN SERVER -------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

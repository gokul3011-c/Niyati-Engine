-- ============================================
-- Niyati Engine - Database Schema
-- Database: PostgreSQL
-- ============================================

-- Create database (run this separately in pgAdmin or psql)
-- CREATE DATABASE "Niyati_Engine";

-- Connect to the database before running the rest
-- \c "Niyati_Engine";

-- ============================================
-- 1. USERS TABLE
-- Stores user authentication information
-- ============================================
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

-- ============================================
-- 2. CANDIDATES TABLE
-- Stores candidate resume analysis results
-- ============================================
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
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

-- ============================================
-- 3. ANALYSIS SESSIONS TABLE
-- Tracks each analysis session
-- ============================================
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

-- ============================================
-- INDEXES FOR BETTER QUERY PERFORMANCE
-- ============================================
CREATE INDEX idx_candidates_user_id ON candidates(user_id);
CREATE INDEX idx_candidates_final_score ON candidates(final_score DESC);
CREATE INDEX idx_candidates_status ON candidates(status);
CREATE INDEX idx_candidates_created_at ON candidates(created_at DESC);
CREATE INDEX idx_analysis_sessions_user_id ON analysis_sessions(user_id);
CREATE INDEX idx_analysis_sessions_created_at ON analysis_sessions(created_at DESC);

-- ============================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================
-- INSERT INTO users (username, password, email) 
-- VALUES ('admin', 'admin123', 'admin@niyati.com');

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- View: User statistics
CREATE OR REPLACE VIEW user_stats AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(DISTINCT a.id) as total_sessions,
    COUNT(DISTINCT c.id) as total_candidates_analyzed,
    COUNT(CASE WHEN c.status = 'accepted' THEN 1 END) as total_accepted,
    COUNT(CASE WHEN c.status = 'rejected' THEN 1 END) as total_rejected,
    AVG(c.final_score) as avg_score
FROM users u
LEFT JOIN analysis_sessions a ON u.id = a.user_id
LEFT JOIN candidates c ON u.id = c.user_id
GROUP BY u.id, u.username;

-- ============================================
-- COMMENTS
-- ============================================
COMMENT ON TABLE users IS 'Stores user authentication and profile data';
COMMENT ON TABLE candidates IS 'Stores candidate resume analysis results';
COMMENT ON TABLE analysis_sessions IS 'Tracks each resume analysis session';

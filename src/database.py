import sqlite3
import pandas as pd
import json
from datetime import datetime
from typing import Optional, List, Dict

DB_FILE = "career_suite.db"

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Table for TalentScout (Recruiter Mode)
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT,
                    email TEXT,
                    position TEXT,
                    tech_stack TEXT,
                    interview_data TEXT, -- JSON dump of the conversation
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

    # Table for PrepMaster (Candidate Mode)
    c.execute('''CREATE TABLE IF NOT EXISTS prep_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    question TEXT,
                    user_answer TEXT,
                    ai_feedback TEXT,
                    score INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    
    # Table for MCQ Quiz Results
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    total_questions INTEGER DEFAULT 10,
                    correct_answers INTEGER,
                    score_percentage REAL,
                    time_taken INTEGER, -- in seconds
                    quiz_data TEXT, -- JSON dump of questions and answers
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    
    conn.commit()
    conn.close()

def save_candidate_profile(data: dict, history: list):
    """Saves a candidate's screening details."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO candidates (full_name, email, position, tech_stack, interview_data)
                 VALUES (?, ?, ?, ?, ?)''', 
                 (data.get('full_name'), data.get('email'), 
                  data.get('position'), data.get('tech_stack'), 
                  json.dumps(history)))
    conn.commit()
    conn.close()

def save_prep_attempt(topic, question, answer, feedback, score):
    """Saves a practice interview attempt."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO prep_history (topic, question, user_answer, ai_feedback, score)
                 VALUES (?, ?, ?, ?, ?)''', (topic, question, answer, feedback, int(score)))
    conn.commit()
    conn.close()

def get_prep_history():
    """Retrieves practice history for analytics."""
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query("SELECT * FROM prep_history ORDER BY timestamp DESC", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

# ============ MCQ Quiz Database Methods ============

def save_quiz_result(language: str, difficulty: str, correct_answers: int, 
                     total_questions: int, quiz_data: dict, time_taken: int = 0):
    """Save MCQ quiz result to database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    score_percentage = (correct_answers / total_questions) * 100
    
    c.execute('''INSERT INTO quiz_results 
                 (language, difficulty, total_questions, correct_answers, 
                  score_percentage, time_taken, quiz_data)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (language, difficulty, total_questions, correct_answers,
                  score_percentage, time_taken, json.dumps(quiz_data)))
    
    conn.commit()
    conn.close()

def get_quiz_history(limit: int = 10) -> pd.DataFrame:
    """Retrieve recent quiz history."""
    conn = sqlite3.connect(DB_FILE)
    try:
        query = f"SELECT * FROM quiz_results ORDER BY timestamp DESC LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

def get_analytics_by_language(language: Optional[str] = None) -> Dict:
    """Get analytics for a specific language or all languages."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if language:
        c.execute('''SELECT AVG(score_percentage) as avg_score, 
                            COUNT(*) as total_attempts,
                            MAX(score_percentage) as best_score,
                            MIN(score_percentage) as worst_score
                     FROM quiz_results WHERE language = ?''', (language,))
    else:
        c.execute('''SELECT language, AVG(score_percentage) as avg_score, 
                            COUNT(*) as total_attempts
                     FROM quiz_results GROUP BY language''')
    
    results = c.fetchall()
    conn.close()
    
    if language and results:
        return {
            'language': language,
            'avg_score': round(results[0][0] or 0, 2),
            'total_attempts': results[0][1],
            'best_score': round(results[0][2] or 0, 2),
            'worst_score': round(results[0][3] or 0, 2)
        }
    elif not language:
        return [{'language': r[0], 'avg_score': round(r[1] or 0, 2), 
                 'total_attempts': r[2]} for r in results]
    return {}

def get_analytics_by_difficulty(difficulty: Optional[str] = None) -> Dict:
    """Get analytics for a specific difficulty level."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if difficulty:
        c.execute('''SELECT AVG(score_percentage) as avg_score, 
                            COUNT(*) as total_attempts
                     FROM quiz_results WHERE difficulty = ?''', (difficulty,))
        result = c.fetchone()
        conn.close()
        return {
            'difficulty': difficulty,
            'avg_score': round(result[0] or 0, 2),
            'total_attempts': result[1]
        }
    else:
        c.execute('''SELECT difficulty, AVG(score_percentage) as avg_score, 
                            COUNT(*) as total_attempts
                     FROM quiz_results GROUP BY difficulty''')
        results = c.fetchall()
        conn.close()
        return [{'difficulty': r[0], 'avg_score': round(r[1] or 0, 2), 
                 'total_attempts': r[2]} for r in results]

def get_overall_analytics() -> Dict:
    """Get overall quiz performance analytics."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('''SELECT COUNT(*) as total_quizzes,
                        AVG(score_percentage) as avg_score,
                        MAX(score_percentage) as best_score,
                        SUM(correct_answers) as total_correct,
                        SUM(total_questions) as total_questions
                 FROM quiz_results''')
    
    result = c.fetchone()
    conn.close()
    
    if result and result[0] > 0:
        return {
            'total_quizzes': result[0],
            'avg_score': round(result[1] or 0, 2),
            'best_score': round(result[2] or 0, 2),
            'total_correct': result[3] or 0,
            'total_questions': result[4] or 0,
            'accuracy': round((result[3] / result[4] * 100) if result[4] > 0 else 0, 2)
        }
    return {
        'total_quizzes': 0,
        'avg_score': 0,
        'best_score': 0,
        'total_correct': 0,
        'total_questions': 0,
        'accuracy': 0
    }

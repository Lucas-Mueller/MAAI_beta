"""
Database operations for CV assessment system.
Uses SQLite for simplicity and cloud compatibility.
"""
import sqlite3
import aiosqlite
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class Database:
    """Handles all database operations for the CV assessment system"""
    
    def __init__(self, db_path: str = "cv_assessment.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
    
    async def init_db(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Job descriptions table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS job_descriptions (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # CVs table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cvs (
                    id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES job_descriptions (id)
                )
            """)
            
            # Evaluations table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cv_id TEXT NOT NULL,
                    skill_score REAL,
                    cultural_score REAL,
                    overall_score REAL,
                    skill_assessment TEXT,
                    cultural_assessment TEXT,
                    summary TEXT,
                    recommendation TEXT,
                    raw_output TEXT,
                    has_error BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cv_id) REFERENCES cvs (id)
                )
            """)
            
            await db.commit()
    
    async def store_job_description(self, job_id: str, text: str, filename: str):
        """Store a job description in the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO job_descriptions (id, text, filename) VALUES (?, ?, ?)",
                (job_id, text, filename)
            )
            await db.commit()
    
    async def store_cv(self, cv_id: str, job_id: str, text: str, filename: str):
        """Store a CV in the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO cvs (id, job_id, text, filename) VALUES (?, ?, ?, ?)",
                (cv_id, job_id, text, filename)
            )
            await db.commit()
    
    async def store_evaluation(self, cv_id: str, evaluation_result: Dict[str, Any]):
        """Store evaluation results in the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO evaluations (
                    cv_id, skill_score, cultural_score, overall_score,
                    skill_assessment, cultural_assessment, summary, 
                    recommendation, raw_output, has_error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cv_id,
                evaluation_result.get('skill_score'),
                evaluation_result.get('cultural_score'),
                evaluation_result.get('overall_score'),
                evaluation_result.get('skill_assessment'),
                evaluation_result.get('cultural_assessment'),
                evaluation_result.get('summary'),
                evaluation_result.get('recommendation'),
                evaluation_result.get('raw_output'),
                evaluation_result.get('error', False)
            ))
            await db.commit()
    
    async def job_exists(self, job_id: str) -> bool:
        """Check if a job description exists"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT 1 FROM job_descriptions WHERE id = ?", (job_id,)
            )
            result = await cursor.fetchone()
            return result is not None
    
    async def get_job_description(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job description by ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, text, filename, created_at FROM job_descriptions WHERE id = ?",
                (job_id,)
            )
            row = await cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'text': row[1],
                    'filename': row[2],
                    'created_at': row[3]
                }
            return None
    
    async def get_cvs_for_job(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all CVs for a specific job"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, text, filename, created_at FROM cvs WHERE job_id = ? ORDER BY created_at",
                (job_id,)
            )
            rows = await cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'text': row[1],
                    'filename': row[2],
                    'created_at': row[3]
                }
                for row in rows
            ]
    
    async def get_evaluation_results(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all evaluation results for a job"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT 
                    c.id, c.filename,
                    e.skill_score, e.cultural_score, e.overall_score,
                    e.skill_assessment, e.cultural_assessment, 
                    e.summary, e.recommendation, e.has_error,
                    e.created_at
                FROM cvs c
                LEFT JOIN evaluations e ON c.id = e.cv_id
                WHERE c.job_id = ?
                ORDER BY e.overall_score DESC, c.filename
            """, (job_id,))
            
            rows = await cursor.fetchall()
            return [
                {
                    'cv_id': row[0],
                    'filename': row[1],
                    'skill_score': row[2],
                    'cultural_score': row[3],
                    'overall_score': row[4],
                    'skill_assessment': row[5],
                    'cultural_assessment': row[6],
                    'summary': row[7],
                    'recommendation': row[8],
                    'has_error': bool(row[9]),
                    'evaluated_at': row[10]
                }
                for row in rows
            ]
    
    async def list_jobs(self) -> List[Dict[str, Any]]:
        """List all job descriptions with CV counts"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT 
                    j.id, j.filename, j.created_at,
                    COUNT(c.id) as cv_count,
                    COUNT(e.id) as evaluated_count
                FROM job_descriptions j
                LEFT JOIN cvs c ON j.id = c.job_id
                LEFT JOIN evaluations e ON c.id = e.cv_id
                GROUP BY j.id, j.filename, j.created_at
                ORDER BY j.created_at DESC
            """)
            
            rows = await cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'filename': row[1],
                    'created_at': row[2],
                    'cv_count': row[3],
                    'evaluated_count': row[4]
                }
                for row in rows
            ]
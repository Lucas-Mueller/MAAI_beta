"""
FastAPI application for CV assessment system.
Handles file uploads, PDF processing, and multi-agent evaluation.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import asyncio
from pathlib import Path
import json
from typing import List, Dict
import uuid
import os

from backend.pdf_processor import PDFProcessor
from backend.cv_evaluator import CVEvaluator
from backend.database import Database

app = FastAPI(title="CV Assessment System", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Initialize components
pdf_processor = PDFProcessor()
cv_evaluator = CVEvaluator()
db = Database()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await db.init_db()

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    """Serve the main frontend page"""
    frontend_path = Path("frontend/index.html")
    if frontend_path.exists():
        return frontend_path.read_text()
    return "<h1>Frontend not found</h1>"

@app.post("/upload/job-description")
async def upload_job_description(file: UploadFile = File(...)):
    """Upload and process job description PDF"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read and process PDF
        content = await file.read()
        job_text = pdf_processor.extract_text_from_pdf(content)
        
        # Store job description
        job_id = str(uuid.uuid4())
        await db.store_job_description(job_id, job_text, file.filename)
        
        return {"job_id": job_id, "message": "Job description uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/upload/cvs/{job_id}")
async def upload_cvs(job_id: str, files: List[UploadFile] = File(...)):
    """Upload and process CV PDFs for a specific job"""
    if not await db.job_exists(job_id):
        raise HTTPException(status_code=404, detail="Job description not found")
    
    uploaded_cvs = []
    
    for file in files:
        if not file.filename.endswith('.pdf'):
            continue
            
        try:
            # Read and process PDF
            content = await file.read()
            cv_text = pdf_processor.extract_text_from_pdf(content)
            
            # Store CV
            cv_id = str(uuid.uuid4())
            await db.store_cv(cv_id, job_id, cv_text, file.filename)
            uploaded_cvs.append({"cv_id": cv_id, "filename": file.filename})
            
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            continue
    
    return {"uploaded_cvs": uploaded_cvs, "message": f"Uploaded {len(uploaded_cvs)} CVs successfully"}

@app.post("/evaluate/{job_id}")
async def evaluate_candidates(job_id: str):
    """Start evaluation process for all CVs under a job"""
    if not await db.job_exists(job_id):
        raise HTTPException(status_code=404, detail="Job description not found")
    
    try:
        # Get job description and CVs
        job_data = await db.get_job_description(job_id)
        cvs = await db.get_cvs_for_job(job_id)
        
        if not cvs:
            raise HTTPException(status_code=400, detail="No CVs found for this job")
        
        # Start evaluation process
        evaluation_results = []
        for cv in cvs:
            result = await cv_evaluator.evaluate_cv(job_data['text'], cv['text'])
            
            # Store evaluation result
            await db.store_evaluation(cv['id'], result)
            evaluation_results.append({
                "cv_id": cv['id'],
                "filename": cv['filename'],
                "status": "completed"
            })
        
        return {"results": evaluation_results, "message": "Evaluation completed"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during evaluation: {str(e)}")

@app.get("/results/{job_id}")
async def get_results(job_id: str):
    """Get evaluation results for a job"""
    if not await db.job_exists(job_id):
        raise HTTPException(status_code=404, detail="Job description not found")
    
    results = await db.get_evaluation_results(job_id)
    return {"results": results}

@app.get("/jobs")
async def list_jobs():
    """List all job descriptions"""
    jobs = await db.list_jobs()
    return {"jobs": jobs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
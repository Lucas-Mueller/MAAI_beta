#!/usr/bin/env python3
"""
CV Assessment System Startup Script
Run this to start the application server
"""
import uvicorn
import os
from pathlib import Path

def main():
    """Start the FastAPI application"""
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    print("🚀 Starting CV Assessment System...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📄 Upload job descriptions and CVs to get started!")
    print("-" * 50)
    
    # Start the server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
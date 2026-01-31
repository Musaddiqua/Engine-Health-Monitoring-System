"""
Vercel Serverless Function for FastAPI Backend
This wraps the FastAPI app for Vercel deployment using Mangum
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the FastAPI app
from api import app

# Create Mangum handler for Vercel
from mangum import Mangum

# Initialize handler
handler = Mangum(app, lifespan="off")

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

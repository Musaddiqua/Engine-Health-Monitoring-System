"""
Main entry point for the Engine Health Monitoring System.
Run this to start the FastAPI server.
"""

import uvicorn

if __name__ == "__main__":
    print("Starting Adaptive Engine Health Monitoring System...")
    print("API will be available at http://localhost:8000")
    print("API Documentation at http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )





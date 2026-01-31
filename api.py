"""
FastAPI REST API Layer
Provides Power BI-ready endpoints for engine health monitoring.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging

from engine_health_service import EngineHealthService
from models import APIResponse, EngineHealthStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Adaptive Engine Health Monitoring System",
    description="AI-powered engine health monitoring using adaptive baseline learning",
    version="1.0.0"
)

# Enable CORS for Power BI and other clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instance (initialized on startup)
service: Optional[EngineHealthService] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the engine health service on startup."""
    global service
    try:
        service = EngineHealthService("engine_telemetry.csv")
        logger.info("API startup complete - Engine Health Service initialized")
    except Exception as e:
        logger.error(f"Failed to initialize service: {str(e)}")
        raise


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Adaptive Engine Health Monitoring System API",
        "version": "1.0.0",
        "endpoints": {
            "/engine-status": "Get engine health status for a vehicle",
            "/vehicles": "Get list of all vehicles",
            "/health": "API health check"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service_initialized": service is not None
    }


@app.get("/vehicles", tags=["Vehicles"], response_model=dict)
async def get_vehicles():
    """
    Get list of all vehicles in the system.
    
    Returns:
        Dictionary with list of vehicle IDs
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        vehicles = service.get_all_vehicles()
        return {
            "success": True,
            "data": {
                "vehicles": vehicles,
                "count": len(vehicles)
            }
        }
    except Exception as e:
        logger.error(f"Error getting vehicles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/engine-status", tags=["Engine Health"], response_model=APIResponse)
async def get_engine_status(
    vehicle_id: str = Query(..., description="Vehicle ID to check", example="VH_01")
):
    """
    Get current engine health status for a vehicle.
    
    This is the main endpoint for Power BI integration.
    Returns comprehensive engine health analysis including:
    - Current telemetry values
    - Expected ranges (learned baselines)
    - Deviation analysis
    - Engine Safety Score (0-100)
    - Human-readable explanations
    
    Args:
        vehicle_id: Vehicle identifier (required)
    
    Returns:
        APIResponse with EngineHealthStatus data
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        status = service.get_engine_status(vehicle_id)
        
        if status is None:
            return APIResponse(
                success=False,
                message=f"Vehicle {vehicle_id} not found or insufficient baseline data"
            )
        
        return APIResponse(
            success=True,
            data=status,
            message="Engine status retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error getting engine status for {vehicle_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/engine-status/batch", tags=["Engine Health"], response_model=dict)
async def get_batch_engine_status(
    vehicle_ids: Optional[str] = Query(None, description="Comma-separated vehicle IDs")
):
    """
    Get engine status for multiple vehicles at once.
    
    Args:
        vehicle_ids: Comma-separated list of vehicle IDs (optional, returns all if not provided)
    
    Returns:
        Dictionary with status for each vehicle
    """
    if service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        if vehicle_ids:
            vehicle_list = [v.strip() for v in vehicle_ids.split(",")]
        else:
            vehicle_list = service.get_all_vehicles()
        
        results = {}
        for vid in vehicle_list:
            status = service.get_engine_status(vid)
            results[vid] = status.dict() if status else None
        
        return {
            "success": True,
            "data": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error in batch status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





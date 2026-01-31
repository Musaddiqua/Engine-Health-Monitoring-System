"""
Data models for the Engine Health Monitoring System.
Defines Pydantic models for API request/response and internal data structures.
"""

from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime


class VehicleProfile(BaseModel):
    """Vehicle metadata profile."""
    vehicle_id: str
    vehicle_type: str  # Car / Bike / Truck
    engine_type: str   # Petrol / Diesel
    engine_cc: float


class TelemetryReading(BaseModel):
    """Single telemetry reading from a vehicle."""
    timestamp: datetime
    vehicle_id: str
    gear: int
    speed_kmph: float
    rpm: float
    engine_temp_c: float
    oil_pressure_psi: float
    vibration: float


class BaselineStats(BaseModel):
    """Learned baseline statistics for a vehicle+gear combination."""
    mean: float
    std: float
    count: int = 0  # Number of samples used to build this baseline


class GearBaseline(BaseModel):
    """Baseline statistics for all metrics in a specific gear."""
    gear: int
    rpm: BaselineStats
    engine_temp: BaselineStats
    oil_pressure: BaselineStats
    vibration: BaselineStats


class DeviationMetrics(BaseModel):
    """Deviation analysis for a single metric."""
    current_value: float
    expected_mean: float
    expected_range_min: float
    expected_range_max: float
    deviation_percent: float
    deviation_std: float  # How many standard deviations away
    status: str  # Normal / Warning / Critical


class EngineHealthStatus(BaseModel):
    """Complete engine health status for API response."""
    vehicle_id: str
    timestamp: datetime
    gear: int
    
    # Current telemetry values
    current_rpm: float
    current_engine_temp: float
    current_oil_pressure: float
    current_vibration: float
    current_speed_kmph: float
    
    # Deviation analysis for each metric
    rpm_deviation: DeviationMetrics
    temp_deviation: DeviationMetrics
    oil_pressure_deviation: DeviationMetrics
    vibration_deviation: DeviationMetrics
    
    # Overall scoring
    engine_safety_score: float = Field(ge=0, le=100)  # 0-100, lower = higher risk
    overall_status: str  # Normal / Warning / Critical
    
    # Explainable AI output
    explanation: str
    recommendations: List[str] = []


class APIResponse(BaseModel):
    """Standard API response format."""
    success: bool
    data: Optional[EngineHealthStatus] = None
    message: Optional[str] = None





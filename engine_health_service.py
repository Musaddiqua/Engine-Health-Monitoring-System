"""
Engine Health Service
Orchestrates all components to provide complete engine health analysis.
"""

from typing import Optional
from datetime import datetime
import logging
import pandas as pd

from data_ingestion import DataIngestion
from baseline_learner import BaselineLearner
from deviation_detector import DeviationDetector
from risk_scorer import RiskScorer
from explainer import ExplainableAI
from models import EngineHealthStatus, DeviationMetrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EngineHealthService:
    """
    Main service that orchestrates all components for engine health monitoring.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize the engine health service.
        
        Args:
            csv_path: Path to engine_telemetry.csv
        """
        self.csv_path = csv_path
        self.data_ingestion = DataIngestion(csv_path)
        self.baseline_learner = BaselineLearner(min_samples=10)
        self.deviation_detector = DeviationDetector()
        self.risk_scorer = RiskScorer()
        self.explainer = ExplainableAI()
        
        # Load data and learn baselines
        self._initialize()
    
    def _initialize(self):
        """Load data and learn initial baselines."""
        logger.info("Initializing Engine Health Service...")
        
        # Load data
        self.data_ingestion.load_data()
        
        # Learn baselines from all historical data
        df = self.data_ingestion.df
        self.baseline_learner.learn_from_data(df)
        
        logger.info("Engine Health Service initialized successfully")
    
    def get_engine_status(self, vehicle_id: str) -> Optional[EngineHealthStatus]:
        """
        Get current engine health status for a vehicle.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            EngineHealthStatus or None if vehicle/gear not found
        """
        # Get latest reading
        latest = self.data_ingestion.get_latest_reading(vehicle_id)
        if latest is None:
            logger.warning(f"No data found for vehicle {vehicle_id}")
            return None
        
        gear = int(latest['gear'])
        
        # Get baseline for this vehicle+gear
        baseline = self.baseline_learner.get_baseline(vehicle_id, gear)
        if baseline is None:
            logger.warning(
                f"No baseline learned for vehicle {vehicle_id}, gear {gear}. "
                f"Need more historical data."
            )
            return None
        
        # Prepare current values
        current_values = {
            'rpm': float(latest['rpm']),
            'engine_temp': float(latest['engine_temp_c']),
            'oil_pressure': float(latest['oil_pressure_psi']),
            'vibration': float(latest['vibration'])
        }
        
        # Analyze deviations
        deviations = self.deviation_detector.analyze_all_metrics(current_values, baseline)
        
        # Calculate risk scores
        safety_score = self.risk_scorer.calculate_engine_safety_score(deviations)
        overall_status = self.risk_scorer.get_overall_status(safety_score)
        
        # Generate explanations
        explanation = self.explainer.generate_explanation(
            deviations, vehicle_id, gear, safety_score, overall_status
        )
        recommendations = self.explainer.generate_recommendations(
            deviations, overall_status
        )
        
        # Build response - handle timestamp conversion
        if isinstance(latest['timestamp'], datetime):
            timestamp = latest['timestamp']
        elif isinstance(latest['timestamp'], pd.Timestamp):
            timestamp = latest['timestamp'].to_pydatetime()
        else:
            timestamp = pd.to_datetime(latest['timestamp']).to_pydatetime()
        
        status = EngineHealthStatus(
            vehicle_id=vehicle_id,
            timestamp=timestamp,
            gear=gear,
            current_rpm=current_values['rpm'],
            current_engine_temp=current_values['engine_temp'],
            current_oil_pressure=current_values['oil_pressure'],
            current_vibration=current_values['vibration'],
            current_speed_kmph=float(latest['speed_kmph']),
            rpm_deviation=deviations['rpm'],
            temp_deviation=deviations['engine_temp'],
            oil_pressure_deviation=deviations['oil_pressure'],
            vibration_deviation=deviations['vibration'],
            engine_safety_score=safety_score,
            overall_status=overall_status,
            explanation=explanation,
            recommendations=recommendations
        )
        
        return status
    
    def get_all_vehicles(self) -> list:
        """Get list of all vehicle IDs."""
        return self.data_ingestion.get_all_vehicle_ids()


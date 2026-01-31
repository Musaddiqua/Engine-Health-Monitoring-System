"""
Risk Scoring System
Calculates individual risk scores and combined Engine Safety Score.
"""

import numpy as np
from typing import Dict
import logging

from models import DeviationMetrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskScorer:
    """
    Calculates risk scores based on deviation metrics.
    Engine Safety Score: 0-100 (lower = higher risk).
    """
    
    def __init__(self):
        """Initialize risk scorer."""
        pass
    
    def calculate_metric_risk_score(self, deviation: DeviationMetrics) -> float:
        """
        Calculate individual risk score for a metric (0-100, lower = higher risk).
        
        Args:
            deviation: DeviationMetrics for a single metric
            
        Returns:
            Risk score between 0-100
        """
        # Base score starts at 100 (perfect)
        base_score = 100.0
        
        # Penalize based on deviation standard deviations
        # Normal (<2 std): 100 points
        # Warning (2-3.5 std): 70-100 points
        # Critical (>3.5 std): 0-70 points
        
        deviation_std = deviation.deviation_std
        
        if deviation.status == "Critical":
            # Critical: score decreases linearly from 70 to 0
            # At 3.5 std: 70 points, at 5 std: 0 points
            if deviation_std >= 5.0:
                score = 0.0
            else:
                # Linear interpolation: 70 at 3.5 std, 0 at 5 std
                score = 70.0 * (1 - (deviation_std - 3.5) / 1.5)
                score = max(0.0, score)
                
        elif deviation.status == "Warning":
            # Warning: score decreases from 100 to 70
            # At 2 std: 100 points, at 3.5 std: 70 points
            score = 100.0 - 30.0 * ((deviation_std - 2.0) / 1.5)
            score = max(70.0, score)
            
        else:  # Normal
            # Normal: full score with slight penalty for any deviation
            # At 0 std: 100 points, at 2 std: 95 points
            # Use absolute value to handle negative deviations (below mean)
            penalty = min(abs(deviation_std) / 2.0, 1.0) * 5.0
            score = 100.0 - penalty
        
        # Cap score at 100 to prevent exceeding maximum
        score = min(100.0, max(0.0, score))
        return round(score, 2)
    
    def calculate_engine_safety_score(self, deviations: Dict[str, DeviationMetrics]) -> float:
        """
        Calculate combined Engine Safety Score from all metrics.
        Uses weighted average with equal weights.
        
        Args:
            deviations: Dictionary with DeviationMetrics for all metrics:
                {'rpm': DeviationMetrics, 'engine_temp': ..., 'oil_pressure': ..., 'vibration': ...}
            
        Returns:
            Engine Safety Score (0-100)
        """
        metric_scores = {}
        
        for metric_name, deviation in deviations.items():
            score = self.calculate_metric_risk_score(deviation)
            metric_scores[metric_name] = score
        
        # Weighted average (equal weights)
        weights = {
            'rpm': 0.25,
            'engine_temp': 0.30,  # Slightly higher weight for temperature
            'oil_pressure': 0.25,
            'vibration': 0.20
        }
        
        total_score = sum(
            metric_scores[metric] * weights[metric] 
            for metric in metric_scores.keys()
        )
        
        # Cap at 100 to ensure it never exceeds maximum
        total_score = min(100.0, max(0.0, total_score))
        return round(total_score, 2)
    
    def get_overall_status(self, safety_score: float) -> str:
        """
        Determine overall status from safety score.
        
        Args:
            safety_score: Engine Safety Score (0-100)
            
        Returns:
            Status: "Normal" / "Warning" / "Critical"
        """
        if safety_score >= 85:
            return "Normal"
        elif safety_score >= 60:
            return "Warning"
        else:
            return "Critical"



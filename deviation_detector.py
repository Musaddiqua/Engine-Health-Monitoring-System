"""
Deviation Detection Engine
Compares current telemetry values against learned baselines.
Detects abnormal behavior using adaptive thresholds.
"""

import numpy as np
from typing import Optional
import logging

from models import GearBaseline, DeviationMetrics, BaselineStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeviationDetector:
    """
    Detects deviations from learned baselines using adaptive thresholds.
    No fixed limits - everything is relative to learned normal behavior.
    """
    
    def __init__(self, 
                 warning_threshold_std: float = 2.0,
                 critical_threshold_std: float = 3.5,
                 warning_threshold_percent: float = 20.0,
                 critical_threshold_percent: float = 40.0):
        """
        Initialize deviation detector.
        
        Args:
            warning_threshold_std: Warning threshold in standard deviations
            critical_threshold_std: Critical threshold in standard deviations
            warning_threshold_percent: Warning threshold as percentage deviation
            critical_threshold_percent: Critical threshold as percentage deviation
        """
        self.warning_threshold_std = warning_threshold_std
        self.critical_threshold_std = critical_threshold_std
        self.warning_threshold_percent = warning_threshold_percent
        self.critical_threshold_percent = critical_threshold_percent
    
    def analyze_deviation(self, 
                         current_value: float,
                         baseline_stats: BaselineStats,
                         metric_name: str = "metric") -> DeviationMetrics:
        """
        Analyze deviation of current value from baseline.
        
        Args:
            current_value: Current telemetry value
            baseline_stats: Learned baseline statistics
            metric_name: Name of the metric (for logging)
            
        Returns:
            DeviationMetrics with analysis results
        """
        mean = baseline_stats.mean
        std = baseline_stats.std
        
        # Calculate deviation in standard deviations
        if std > 0:
            deviation_std = abs(current_value - mean) / std
        else:
            deviation_std = 0.0
        
        # Calculate percentage deviation
        if mean != 0:
            deviation_percent = abs((current_value - mean) / mean) * 100
        else:
            deviation_percent = 0.0
        
        # Determine status based on adaptive thresholds
        # Use the more conservative (stricter) threshold
        if deviation_std >= self.critical_threshold_std or deviation_percent >= self.critical_threshold_percent:
            status = "Critical"
        elif deviation_std >= self.warning_threshold_std or deviation_percent >= self.warning_threshold_percent:
            status = "Warning"
        else:
            status = "Normal"
        
        # Expected range (mean ± 2*std for visualization)
        expected_range_min = mean - 2 * std
        expected_range_max = mean + 2 * std
        
        return DeviationMetrics(
            current_value=current_value,
            expected_mean=mean,
            expected_range_min=max(0, expected_range_min),  # Ensure non-negative for physical metrics
            expected_range_max=expected_range_max,
            deviation_percent=deviation_percent,
            deviation_std=deviation_std,
            status=status
        )
    
    def analyze_all_metrics(self, 
                           current_values: dict,
                           baseline: GearBaseline) -> dict:
        """
        Analyze all metrics at once.
        
        Args:
            current_values: Dictionary with current values:
                {'rpm': float, 'engine_temp': float, 'oil_pressure': float, 'vibration': float}
            baseline: GearBaseline with learned statistics
            
        Returns:
            Dictionary with DeviationMetrics for each metric
        """
        return {
            'rpm': self.analyze_deviation(
                current_values['rpm'], 
                baseline.rpm, 
                'RPM'
            ),
            'engine_temp': self.analyze_deviation(
                current_values['engine_temp'], 
                baseline.engine_temp, 
                'Engine Temperature'
            ),
            'oil_pressure': self.analyze_deviation(
                current_values['oil_pressure'], 
                baseline.oil_pressure, 
                'Oil Pressure'
            ),
            'vibration': self.analyze_deviation(
                current_values['vibration'], 
                baseline.vibration, 
                'Vibration'
            )
        }


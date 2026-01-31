"""
Explainable AI Layer
Generates human-readable explanations for engine health status.
Critical for non-technical users and judges.
"""

from typing import Dict, List
import logging

from models import DeviationMetrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplainableAI:
    """
    Generates explainable, human-readable explanations for engine health.
    Avoids black-box decisions.
    """
    
    def __init__(self):
        """Initialize explainable AI layer."""
        # Friendly metric names
        self.metric_names = {
            'rpm': 'RPM',
            'engine_temp': 'Engine Temperature',
            'oil_pressure': 'Oil Pressure',
            'vibration': 'Vibration'
        }
    
    def generate_explanation(self, 
                            deviations: Dict[str, DeviationMetrics],
                            vehicle_id: str,
                            gear: int,
                            safety_score: float,
                            overall_status: str) -> str:
        """
        Generate main explanation text for the engine status.
        
        Args:
            deviations: Dictionary with DeviationMetrics for all metrics
            vehicle_id: Vehicle identifier
            gear: Current gear
            safety_score: Engine Safety Score
            overall_status: Overall status (Normal/Warning/Critical)
            
        Returns:
            Human-readable explanation string
        """
        explanations = []
        
        # Start with overall status
        if overall_status == "Normal":
            explanations.append(
                f"Engine is operating normally for this vehicle in gear {gear}. "
                f"All metrics are within expected ranges based on learned baseline behavior."
            )
        elif overall_status == "Warning":
            explanations.append(
                f"Engine shows warning signs. Some metrics are deviating from normal "
                f"behavior for this vehicle in gear {gear}."
            )
        else:  # Critical
            explanations.append(
                f"Engine shows critical deviations from normal behavior for this vehicle "
                f"in gear {gear}. Immediate attention recommended."
            )
        
        # Add specific metric explanations for non-normal statuses
        non_normal_metrics = [
            (name, dev) for name, dev in deviations.items() 
            if dev.status != "Normal"
        ]
        
        if non_normal_metrics:
            explanations.append("\nSpecific deviations detected:")
            for metric_name, deviation in non_normal_metrics:
                metric_explanation = self._explain_metric_deviation(
                    metric_name, deviation, gear
                )
                explanations.append(f"• {metric_explanation}")
        else:
            explanations.append(
                "All metrics (RPM, Temperature, Oil Pressure, Vibration) are within "
                "expected ranges for this vehicle."
            )
        
        # Add safety score context
        if safety_score < 60:
            explanations.append(
                f"\nEngine Safety Score: {safety_score:.1f}/100 - Critical risk level."
            )
        elif safety_score < 85:
            explanations.append(
                f"\nEngine Safety Score: {safety_score:.1f}/100 - Warning level. "
                f"Monitor closely."
            )
        else:
            explanations.append(
                f"\nEngine Safety Score: {safety_score:.1f}/100 - Healthy operation."
            )
        
        return " ".join(explanations)
    
    def _explain_metric_deviation(self, 
                                  metric_name: str,
                                  deviation: DeviationMetrics,
                                  gear: int) -> str:
        """
        Generate explanation for a single metric deviation.
        
        Args:
            metric_name: Name of the metric
            deviation: DeviationMetrics for this metric
            gear: Current gear
            
        Returns:
            Explanation string
        """
        friendly_name = self.metric_names.get(metric_name, metric_name)
        direction = "higher" if deviation.current_value > deviation.expected_mean else "lower"
        
        # Create explanation based on status
        if deviation.status == "Critical":
            return (
                f"{friendly_name} is {deviation.deviation_percent:.1f}% {direction} than "
                f"normal for this vehicle in gear {gear} (Expected: {deviation.expected_mean:.1f}, "
                f"Current: {deviation.current_value:.1f}). This is a critical deviation."
            )
        else:  # Warning
            return (
                f"{friendly_name} is {deviation.deviation_percent:.1f}% {direction} than "
                f"normal for this vehicle in gear {gear} (Expected: ~{deviation.expected_mean:.1f}). "
                f"Monitor for trends."
            )
    
    def generate_recommendations(self, 
                                deviations: Dict[str, DeviationMetrics],
                                overall_status: str) -> List[str]:
        """
        Generate actionable recommendations based on deviations.
        
        Args:
            deviations: Dictionary with DeviationMetrics for all metrics
            overall_status: Overall status
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if overall_status == "Normal":
            recommendations.append("Continue normal operation and monitoring.")
            return recommendations
        
        # Check for critical metrics
        critical_metrics = [
            name for name, dev in deviations.items() 
            if dev.status == "Critical"
        ]
        
        if 'engine_temp' in critical_metrics:
            recommendations.append(
                "Check engine cooling system. High temperature deviation may indicate "
                "cooling issues or excessive load."
            )
        
        if 'oil_pressure' in critical_metrics:
            recommendations.append(
                "Inspect oil system. Check oil level and pressure regulation. "
                "Low pressure can cause engine damage."
            )
        
        if 'vibration' in critical_metrics:
            recommendations.append(
                "Investigate vibration sources. Excessive vibration may indicate "
                "mechanical issues or imbalance."
            )
        
        if 'rpm' in critical_metrics:
            recommendations.append(
                "Monitor RPM patterns. Unusual RPM behavior may indicate transmission "
                "or engine control issues."
            )
        
        if overall_status == "Warning":
            recommendations.append(
                "Continue monitoring. If deviations persist or worsen, consider "
                "professional inspection."
            )
        else:  # Critical
            recommendations.append(
                "Immediate professional inspection recommended to prevent potential damage."
            )
        
        return recommendations





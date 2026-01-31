"""
Baseline Learning Engine (CORE AI LOGIC)
Learns adaptive baselines for each vehicle+gear combination.
Uses rolling statistics to build normal behavior profiles.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from collections import defaultdict
import logging

from models import GearBaseline, BaselineStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaselineLearner:
    """
    Learns and maintains adaptive baselines per vehicle+gear combination.
    Uses rolling window statistics to update baselines dynamically.
    """
    
    def __init__(self, min_samples: int = 10, window_size: Optional[int] = None):
        """
        Initialize baseline learner.
        
        Args:
            min_samples: Minimum number of samples before baseline is considered valid
            window_size: Rolling window size (None = use all available data)
        """
        self.min_samples = min_samples
        self.window_size = window_size
        
        # Store baselines: {vehicle_id: {gear: GearBaseline}}
        self.baselines: Dict[str, Dict[int, GearBaseline]] = defaultdict(dict)
        
        # Store raw data for rolling calculations
        self.data_history: Dict[str, Dict[int, Dict[str, list]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )
    
    def learn_from_data(self, df: pd.DataFrame):
        """
        Learn baselines from entire dataset.
        Processes data vehicle by vehicle, gear by gear.
        
        Args:
            df: DataFrame with telemetry data
        """
        logger.info("Starting baseline learning from dataset...")
        
        # Process each vehicle independently
        for vehicle_id in df['vehicle_id'].unique():
            vehicle_df = df[df['vehicle_id'] == vehicle_id].copy()
            
            # Process each gear separately
            for gear in sorted(vehicle_df['gear'].unique()):
                gear_df = vehicle_df[vehicle_df['gear'] == gear].copy()
                
                if len(gear_df) < self.min_samples:
                    logger.warning(
                        f"Vehicle {vehicle_id}, Gear {gear}: Only {len(gear_df)} samples "
                        f"(need {self.min_samples} minimum). Skipping baseline."
                    )
                    continue
                
                # Calculate baseline statistics
                baseline = self._calculate_baseline(gear_df, vehicle_id, gear)
                self.baselines[vehicle_id][gear] = baseline
                
                logger.info(
                    f"Learned baseline for Vehicle {vehicle_id}, Gear {gear}: "
                    f"RPM={baseline.rpm.mean:.1f}±{baseline.rpm.std:.1f}, "
                    f"Temp={baseline.engine_temp.mean:.1f}±{baseline.engine_temp.std:.1f}"
                )
        
        logger.info(f"Baseline learning complete for {len(self.baselines)} vehicles")
    
    def _calculate_baseline(self, gear_df: pd.DataFrame, vehicle_id: str, gear: int) -> GearBaseline:
        """
        Calculate baseline statistics for a vehicle+gear combination.
        
        Args:
            gear_df: DataFrame filtered to this vehicle+gear
            vehicle_id: Vehicle identifier
            gear: Gear number
            
        Returns:
            GearBaseline with statistics for all metrics
        """
        # Use rolling window if specified, otherwise use all data
        if self.window_size and len(gear_df) > self.window_size:
            gear_df = gear_df.tail(self.window_size)
        
        # Calculate mean and std for each metric
        metrics = {
            'rpm': gear_df['rpm'],
            'engine_temp': gear_df['engine_temp_c'],
            'oil_pressure': gear_df['oil_pressure_psi'],
            'vibration': gear_df['vibration']
        }
        
        baseline_dict = {}
        for metric_name, series in metrics.items():
            mean_val = float(series.mean())
            std_val = float(series.std())
            
            # Handle edge case: zero std (all values identical)
            if std_val == 0:
                std_val = mean_val * 0.05  # Use 5% of mean as minimum std
                logger.warning(
                    f"Vehicle {vehicle_id}, Gear {gear}, {metric_name}: "
                    f"Zero std detected, using {std_val:.2f} as minimum"
                )
            
            baseline_dict[metric_name] = BaselineStats(
                mean=mean_val,
                std=std_val,
                count=len(series)
            )
        
        return GearBaseline(
            gear=gear,
            rpm=baseline_dict['rpm'],
            engine_temp=baseline_dict['engine_temp'],
            oil_pressure=baseline_dict['oil_pressure'],
            vibration=baseline_dict['vibration']
        )
    
    def update_baseline_incremental(self, vehicle_id: str, gear: int, 
                                   rpm: float, temp: float, 
                                   oil_pressure: float, vibration: float):
        """
        Update baseline incrementally with new reading.
        Uses exponential moving average for efficiency.
        
        Args:
            vehicle_id: Vehicle identifier
            gear: Gear number
            rpm: Current RPM value
            temp: Current engine temperature
            oil_pressure: Current oil pressure
            vibration: Current vibration value
        """
        # Store in history
        self.data_history[vehicle_id][gear]['rpm'].append(rpm)
        self.data_history[vehicle_id][gear]['engine_temp'].append(temp)
        self.data_history[vehicle_id][gear]['oil_pressure'].append(oil_pressure)
        self.data_history[vehicle_id][gear]['vibration'].append(vibration)
        
        # Apply window limit if specified
        if self.window_size:
            for metric in ['rpm', 'engine_temp', 'oil_pressure', 'vibration']:
                history = self.data_history[vehicle_id][gear][metric]
                if len(history) > self.window_size:
                    self.data_history[vehicle_id][gear][metric] = history[-self.window_size:]
        
        # Recalculate baseline if we have enough samples
        if len(self.data_history[vehicle_id][gear]['rpm']) >= self.min_samples:
            # Convert to DataFrame for calculation
            data_dict = {
                'rpm': self.data_history[vehicle_id][gear]['rpm'],
                'engine_temp_c': self.data_history[vehicle_id][gear]['engine_temp'],
                'oil_pressure_psi': self.data_history[vehicle_id][gear]['oil_pressure'],
                'vibration': self.data_history[vehicle_id][gear]['vibration']
            }
            temp_df = pd.DataFrame(data_dict)
            
            baseline = self._calculate_baseline(temp_df, vehicle_id, gear)
            self.baselines[vehicle_id][gear] = baseline
    
    def get_baseline(self, vehicle_id: str, gear: int) -> Optional[GearBaseline]:
        """
        Get baseline for a vehicle+gear combination.
        
        Args:
            vehicle_id: Vehicle identifier
            gear: Gear number
            
        Returns:
            GearBaseline or None if not available
        """
        return self.baselines.get(vehicle_id, {}).get(gear)
    
    def has_baseline(self, vehicle_id: str, gear: int) -> bool:
        """Check if baseline exists for vehicle+gear."""
        return gear in self.baselines.get(vehicle_id, {})





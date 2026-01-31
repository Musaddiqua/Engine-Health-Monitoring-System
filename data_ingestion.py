"""
Data Ingestion Layer
Loads and processes engine telemetry data from CSV.
"""

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataIngestion:
    """Handles loading and preprocessing of telemetry data."""
    
    def __init__(self, csv_path: str):
        """
        Initialize data ingestion.
        
        Args:
            csv_path: Path to engine_telemetry.csv file
        """
        self.csv_path = csv_path
        self.df: Optional[pd.DataFrame] = None
        self.vehicle_profiles: Dict[str, Dict] = {}
    
    def load_data(self) -> pd.DataFrame:
        """
        Load telemetry data from CSV file.
        
        Returns:
            DataFrame with telemetry data
        """
        try:
            self.df = pd.read_csv(self.csv_path)
            
            # Convert timestamp to datetime
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            
            # Sort by vehicle_id, timestamp for proper processing order
            self.df = self.df.sort_values(['vehicle_id', 'timestamp'])
            
            logger.info(f"Loaded {len(self.df)} telemetry records from {self.csv_path}")
            logger.info(f"Found {self.df['vehicle_id'].nunique()} unique vehicles")
            
            # Extract vehicle profiles
            self._extract_vehicle_profiles()
            
            return self.df
            
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _extract_vehicle_profiles(self):
        """Extract unique vehicle metadata profiles."""
        profile_cols = ['vehicle_id', 'vehicle_type', 'engine_type', 'engine_cc']
        
        # Get first record per vehicle for metadata
        vehicle_first = self.df.groupby('vehicle_id')[profile_cols].first()
        
        for vehicle_id, row in vehicle_first.iterrows():
            self.vehicle_profiles[vehicle_id] = {
                'vehicle_type': row['vehicle_type'],
                'engine_type': row['engine_type'],
                'engine_cc': float(row['engine_cc'])
            }
        
        logger.info(f"Extracted profiles for {len(self.vehicle_profiles)} vehicles")
    
    def get_vehicle_data(self, vehicle_id: str) -> pd.DataFrame:
        """
        Get all telemetry data for a specific vehicle.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            DataFrame filtered to this vehicle
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        vehicle_df = self.df[self.df['vehicle_id'] == vehicle_id].copy()
        return vehicle_df
    
    def get_latest_reading(self, vehicle_id: str) -> Optional[Dict]:
        """
        Get the most recent telemetry reading for a vehicle.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            Dictionary with latest reading or None if not found
        """
        vehicle_df = self.get_vehicle_data(vehicle_id)
        
        if len(vehicle_df) == 0:
            return None
        
        latest = vehicle_df.iloc[-1].to_dict()
        return latest
    
    def get_vehicle_profile(self, vehicle_id: str) -> Optional[Dict]:
        """
        Get vehicle metadata profile.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            Dictionary with vehicle profile or None if not found
        """
        return self.vehicle_profiles.get(vehicle_id)
    
    def get_all_vehicle_ids(self) -> List[str]:
        """Get list of all vehicle IDs in the dataset."""
        if self.df is None:
            return []
        return sorted(self.df['vehicle_id'].unique().tolist())





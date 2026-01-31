"""
Script to generate sample engine_telemetry.csv for testing.
Creates realistic telemetry data for multiple vehicles across different gears.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_records: int = 2000, output_file: str = "engine_telemetry.csv"):
    """
    Generate sample engine telemetry data.
    
    Args:
        num_records: Number of records to generate
        output_file: Output CSV filename
    """
    np.random.seed(42)
    random.seed(42)
    
    # Define vehicle profiles
    vehicles = [
        {"id": "VH_01", "type": "Car", "engine": "Petrol", "cc": 1500.0},
        {"id": "VH_02", "type": "Car", "engine": "Diesel", "cc": 2000.0},
        {"id": "VH_03", "type": "Bike", "engine": "Petrol", "cc": 250.0},
        {"id": "VH_04", "type": "Truck", "engine": "Diesel", "cc": 3500.0},
        {"id": "VH_05", "type": "Car", "engine": "Petrol", "cc": 1800.0},
    ]
    
    # Gear-specific baseline parameters (vehicle-dependent)
    # Format: {vehicle_type: {gear: {metric: (mean, std)}}}
    gear_baselines = {
        "Car": {
            1: {"rpm": (1500, 200), "temp": (85, 5), "oil": (45, 5), "vib": (2.5, 0.5)},
            2: {"rpm": (2000, 250), "temp": (88, 6), "oil": (48, 6), "vib": (3.0, 0.6)},
            3: {"rpm": (2500, 300), "temp": (90, 7), "oil": (50, 7), "vib": (3.5, 0.7)},
            4: {"rpm": (2200, 280), "temp": (92, 8), "oil": (52, 8), "vib": (4.0, 0.8)},
            5: {"rpm": (2000, 250), "temp": (93, 9), "oil": (50, 9), "vib": (3.8, 0.8)},
        },
        "Bike": {
            1: {"rpm": (2000, 300), "temp": (75, 8), "oil": (35, 4), "vib": (4.5, 1.0)},
            2: {"rpm": (3000, 400), "temp": (78, 9), "oil": (38, 5), "vib": (5.0, 1.2)},
            3: {"rpm": (4000, 500), "temp": (80, 10), "oil": (40, 6), "vib": (5.5, 1.3)},
            4: {"rpm": (4500, 600), "temp": (82, 11), "oil": (42, 7), "vib": (6.0, 1.4)},
            5: {"rpm": (5000, 700), "temp": (85, 12), "oil": (40, 8), "vib": (5.8, 1.5)},
        },
        "Truck": {
            1: {"rpm": (1000, 150), "temp": (90, 6), "oil": (55, 8), "vib": (5.5, 1.2)},
            2: {"rpm": (1300, 180), "temp": (93, 7), "oil": (58, 9), "vib": (6.0, 1.3)},
            3: {"rpm": (1600, 220), "temp": (95, 8), "oil": (60, 10), "vib": (6.5, 1.4)},
            4: {"rpm": (1800, 250), "temp": (97, 9), "oil": (62, 11), "vib": (7.0, 1.5)},
            5: {"rpm": (2000, 280), "temp": (98, 10), "oil": (60, 12), "vib": (6.8, 1.6)},
            6: {"rpm": (1900, 260), "temp": (99, 11), "oil": (58, 13), "vib": (6.5, 1.5)},
        }
    }
    
    records = []
    start_time = datetime(2024, 1, 1, 8, 0, 0)
    
    # Distribute records across vehicles
    records_per_vehicle = num_records // len(vehicles)
    
    for vehicle in vehicles:
        vehicle_id = vehicle["id"]
        vehicle_type = vehicle["type"]
        engine_type = vehicle["engine"]
        engine_cc = vehicle["cc"]
        
        # Get available gears for this vehicle type
        available_gears = list(gear_baselines[vehicle_type].keys())
        
        # Generate records for this vehicle
        for i in range(records_per_vehicle):
            # Simulate time progression
            timestamp = start_time + timedelta(
                seconds=i * 30 + random.randint(0, 60),
                days=random.randint(0, 30)
            )
            
            # Random gear selection
            gear = random.choice(available_gears)
            
            # Get baseline for this gear
            baseline = gear_baselines[vehicle_type][gear]
            
            # Generate values around baseline (with some variation)
            rpm_mean, rpm_std = baseline["rpm"]
            temp_mean, temp_std = baseline["temp"]
            oil_mean, oil_std = baseline["oil"]
            vib_mean, vib_std = baseline["vib"]
            
            # Generate with some normal variation + occasional anomalies
            if random.random() < 0.05:  # 5% chance of slight anomaly
                anomaly_factor = 1.5
            else:
                anomaly_factor = 1.0
            
            rpm = max(500, np.random.normal(rpm_mean, rpm_std * anomaly_factor))
            engine_temp = max(60, np.random.normal(temp_mean, temp_std * anomaly_factor))
            oil_pressure = max(20, np.random.normal(oil_mean, oil_std * anomaly_factor))
            vibration = max(0.5, np.random.normal(vib_mean, vib_std * anomaly_factor))
            
            # Speed roughly correlates with gear and RPM
            speed_base = gear * 15 + (rpm / 100) * 0.5
            speed_kmph = max(0, np.random.normal(speed_base, 5))
            speed_kmph = min(speed_kmph, 150)  # Cap at 150 kmph
            
            records.append({
                "timestamp": timestamp.isoformat(),
                "vehicle_id": vehicle_id,
                "vehicle_type": vehicle_type,
                "engine_type": engine_type,
                "engine_cc": engine_cc,
                "gear": gear,
                "speed_kmph": round(speed_kmph, 2),
                "rpm": round(rpm, 1),
                "engine_temp_c": round(engine_temp, 1),
                "oil_pressure_psi": round(oil_pressure, 1),
                "vibration": round(vibration, 2)
            })
    
    # Create DataFrame and save
    df = pd.DataFrame(records)
    df = df.sort_values(['vehicle_id', 'timestamp'])
    df.to_csv(output_file, index=False)
    
    print(f"Generated {len(df)} records in {output_file}")
    print(f"Vehicles: {df['vehicle_id'].nunique()}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"\nRecords per vehicle:")
    print(df['vehicle_id'].value_counts())


if __name__ == "__main__":
    generate_sample_data(num_records=2000)
    print("\nSample data generation complete!")
    print("You can now run the API server with: python main.py")





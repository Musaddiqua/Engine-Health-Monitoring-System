"""
Quick test script to verify the system works correctly.
Run this after installing dependencies to test the baseline learning and status retrieval.
"""

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from data_ingestion import DataIngestion
        from baseline_learner import BaselineLearner
        from deviation_detector import DeviationDetector
        from risk_scorer import RiskScorer
        from explainer import ExplainableAI
        from engine_health_service import EngineHealthService
        from models import EngineHealthStatus
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False


def test_data_loading():
    """Test data loading."""
    print("\nTesting data loading...")
    try:
        from data_ingestion import DataIngestion
        ingestion = DataIngestion("engine_telemetry.csv")
        df = ingestion.load_data()
        print(f"✓ Loaded {len(df)} records")
        print(f"✓ Found {df['vehicle_id'].nunique()} vehicles")
        return True
    except Exception as e:
        print(f"✗ Data loading error: {e}")
        return False


def test_baseline_learning():
    """Test baseline learning."""
    print("\nTesting baseline learning...")
    try:
        from data_ingestion import DataIngestion
        from baseline_learner import BaselineLearner
        
        ingestion = DataIngestion("engine_telemetry.csv")
        df = ingestion.load_data()
        
        learner = BaselineLearner(min_samples=10)
        learner.learn_from_data(df)
        
        # Check if baselines were learned
        vehicle_ids = df['vehicle_id'].unique()
        baseline_count = 0
        for vid in vehicle_ids[:2]:  # Check first 2 vehicles
            vehicle_df = df[df['vehicle_id'] == vid]
            for gear in vehicle_df['gear'].unique():
                if learner.has_baseline(vid, gear):
                    baseline_count += 1
        
        print(f"✓ Learned {baseline_count} baselines")
        return True
    except Exception as e:
        print(f"✗ Baseline learning error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_engine_status():
    """Test engine status retrieval."""
    print("\nTesting engine status retrieval...")
    try:
        from engine_health_service import EngineHealthService
        
        service = EngineHealthService("engine_telemetry.csv")
        
        # Get status for first vehicle
        vehicles = service.get_all_vehicles()
        if len(vehicles) > 0:
            status = service.get_engine_status(vehicles[0])
            if status:
                print(f"✓ Retrieved status for {vehicles[0]}")
                print(f"  - Gear: {status.gear}")
                print(f"  - Safety Score: {status.engine_safety_score}")
                print(f"  - Status: {status.overall_status}")
                return True
            else:
                print(f"✗ No status returned for {vehicles[0]}")
                return False
        else:
            print("✗ No vehicles found")
            return False
    except Exception as e:
        print(f"✗ Engine status error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Engine Health Monitoring System - Test Suite")
    print("=" * 50)
    
    results = []
    results.append(test_imports())
    results.append(test_data_loading())
    results.append(test_baseline_learning())
    results.append(test_engine_status())
    
    print("\n" + "=" * 50)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 50)
    
    if all(results):
        print("\n✓ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Start the API server: python main.py")
        print("  2. Visit http://localhost:8000/docs for API documentation")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")





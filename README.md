
# Adaptive Engine Health Monitoring System

**Imagine Cup 2026 Project**

An AI-powered engine health monitoring system that learns vehicle-specific baselines and provides real-time, explainable engine health insights. The system adapts to each vehicle's unique behavior patterns instead of relying on fixed manufacturer thresholds.

## 🎯 Key Features

- **Adaptive Baseline Learning**: Learns normal behavior per vehicle+gear combination
- **Context-Aware Analysis**: Models engine behavior by gear for accurate detection
- **Explainable AI**: Human-readable explanations for all alerts and insights
- **No Fixed Thresholds**: All decisions based on learned patterns, not manufacturer specs
- **Power BI Ready**: REST API designed for seamless Power BI integration
- **Real-Time Monitoring**: Fast, efficient processing for live telemetry streams

## 🏗️ System Architecture

### Core Components

1. **Data Ingestion Layer** (`data_ingestion.py`)
   - Loads and processes CSV telemetry data
   - Manages vehicle profiles and metadata

2. **Baseline Learning Engine** (`baseline_learner.py`)
   - Learns rolling mean and standard deviation per vehicle+gear
   - Updates dynamically as new data arrives
   - Core AI logic for understanding "normal" behavior

3. **Deviation Detection Engine** (`deviation_detector.py`)
   - Compares current values against learned baselines
   - Uses adaptive thresholds (standard deviations + percentages)
   - No fixed limits - everything is relative to learned behavior

4. **Risk Scoring System** (`risk_scorer.py`)
   - Calculates individual metric risk scores
   - Combines into Engine Safety Score (0-100, lower = higher risk)
   - Determines overall status: Normal / Warning / Critical

5. **Explainable AI Layer** (`explainer.py`)
   - Generates human-readable explanations
   - Provides actionable recommendations
   - Critical for non-technical users and judges

6. **FastAPI REST API** (`api.py`)
   - RESTful endpoints for Power BI integration
   - JSON responses with complete engine health status
   - Comprehensive API documentation

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data (if needed)

If you don't have `engine_telemetry.csv`, generate sample data:

```bash
python generate_sample_data.py
```

This creates a CSV with 2000 records across 5 vehicles (Cars, Bikes, Trucks).

### 3. Start the API Server

```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 4. Test the API

**Get engine status for a vehicle:**
```bash
curl http://localhost:8000/engine-status?vehicle_id=VH_01
```

**Get list of all vehicles:**
```bash
curl http://localhost:8000/vehicles
```

**Health check:**
```bash
curl http://localhost:8000/health
```

## 📊 API Endpoints

### `GET /engine-status`
Get current engine health status for a vehicle.

**Parameters:**
- `vehicle_id` (required): Vehicle identifier (e.g., "VH_01")

**Response includes:**
- Current telemetry values (RPM, temperature, oil pressure, vibration)
- Expected ranges (learned baselines)
- Deviation percentages and standard deviations
- Engine Safety Score (0-100)
- Overall status (Normal/Warning/Critical)
- Human-readable explanation
- Recommendations

**Example:**
```json
{
  "success": true,
  "data": {
    "vehicle_id": "VH_01",
    "gear": 3,
    "engine_safety_score": 87.5,
    "overall_status": "Normal",
    "explanation": "Engine is operating normally...",
    "rpm_deviation": {
      "current_value": 2450.0,
      "expected_mean": 2500.0,
      "deviation_percent": 2.0,
      "status": "Normal"
    },
    ...
  }
}
```

### `GET /vehicles`
Get list of all vehicles in the system.

### `GET /engine-status/batch`
Get status for multiple vehicles at once.

### `GET /health`
API health check endpoint.

## 🔬 How It Works

### Baseline Learning

The system learns baselines independently for each **vehicle + gear** combination:

1. **Data Segmentation**: Telemetry data is grouped by `vehicle_id` and `gear`
2. **Statistical Learning**: For each combination, calculates:
   - Mean (expected value)
   - Standard deviation (expected variation)
3. **Minimum Samples**: Requires at least 10 samples before baseline is considered valid
4. **Dynamic Updates**: Baselines update as new data arrives

### Deviation Detection

Instead of fixed thresholds like "RPM must be 2000", the system uses:

- **Standard Deviation Thresholds**: 
  - Warning: >2 standard deviations from mean
  - Critical: >3.5 standard deviations from mean
- **Percentage Thresholds**:
  - Warning: >20% deviation from mean
  - Critical: >40% deviation from mean
- **Adaptive**: Uses the more conservative (stricter) threshold

### Risk Scoring

**Engine Safety Score (0-100)**:
- **85-100**: Normal operation
- **60-84**: Warning level
- **0-59**: Critical risk

Individual metric scores are weighted and combined:
- Engine Temperature: 30%
- RPM: 25%
- Oil Pressure: 25%
- Vibration: 20%

### Explainability

Every status includes:
- **Main Explanation**: Overall status in plain language
- **Specific Deviations**: Detailed explanation for each abnormal metric
- **Recommendations**: Actionable next steps

Example: *"Vibration is 62% higher than normal for this vehicle in gear 3 (Expected: ~3.5, Current: 5.7). This is a critical deviation."*

## 📁 Project Structure

```
engine/
├── api.py                      # FastAPI REST API
├── baseline_learner.py         # Core AI: Baseline learning engine
├── data_ingestion.py           # CSV loading and preprocessing
├── deviation_detector.py       # Deviation detection logic
├── engine_health_service.py    # Main orchestration service
├── explainer.py                # Explainable AI layer
├── generate_sample_data.py     # Sample data generator
├── main.py                     # Entry point
├── models.py                   # Pydantic data models
├── risk_scorer.py              # Risk scoring system
├── requirements.txt            # Python dependencies
├── engine_telemetry.csv        # Input data (generated)
└── README.md                   # This file
```

## 🎓 Key Design Principles

1. **No Fixed Thresholds**: All decisions based on learned patterns
2. **Context-Aware**: Gear-specific baselines for accurate detection
3. **Vehicle-Specific**: Each vehicle learns its own "normal"
4. **Explainable**: Every decision has a human-readable explanation
5. **Production-Ready**: Clean, modular, well-documented code
6. **Scalable**: Designed for cloud deployment (Azure/Docker friendly)

## 🔄 Data Format

### Input CSV (`engine_telemetry.csv`)

Required columns:
- `timestamp`: ISO format datetime
- `vehicle_id`: Unique vehicle identifier
- `vehicle_type`: Car / Bike / Truck
- `engine_type`: Petrol / Diesel
- `engine_cc`: Engine displacement
- `gear`: Gear number (1-6)
- `speed_kmph`: Vehicle speed
- `rpm`: Engine RPM
- `engine_temp_c`: Engine temperature (°C)
- `oil_pressure_psi`: Oil pressure (PSI)
- `vibration`: Vibration level

### Output JSON Format

See `/engine-status` endpoint response structure in API documentation.

## 🚀 Deployment

### Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t engine-health-api .
docker run -p 8000:8000 engine-health-api
```

### Azure Deployment

1. Create Azure App Service
2. Configure Python runtime (3.9+)
3. Deploy code
4. Set environment variables if needed
5. Ensure `engine_telemetry.csv` is available

## 🧪 Testing

Test with sample data:
```bash
# Generate sample data
python generate_sample_data.py

# Start API
python main.py

# Test endpoints
curl http://localhost:8000/engine-status?vehicle_id=VH_01
```

## 📝 Notes for Judges

### Innovation
- **Adaptive Learning**: System learns from data, not fixed specs
- **Context Modeling**: Gear-aware analysis for real-world accuracy
- **Explainable AI**: Transparent decision-making for trust

### Technical Excellence
- **Clean Architecture**: Modular, maintainable code
- **Best Practices**: Type hints, error handling, logging
- **API Design**: RESTful, well-documented, Power BI ready

### Real-World Applicability
- **No Manufacturer Data Needed**: Works with any vehicle
- **Scalable**: Handles multiple vehicles, real-time streams
- **Production-Ready**: Cloud deployment friendly

## 👥 Team & Credits

Built for Imagine Cup 2026.
@SameerHawal - Data Analytics 
@Musaddiqua - Machine learning and Testing, UI


---

**Questions?** Check the API documentation at http://localhost:8000/docs when the server is running.

=======
# Engine-Health-Monitoring-System-engine
a5aad912697dac7af9f106ab09768946eb819878

# Adaptive Engine Health Monitoring System - Project Output

## System Overview

**Project Title:** Adaptive Engine Health Monitoring System using AI Baseline Learning

**Status:** ✅ **SYSTEM OPERATIONAL**

The system successfully analyzes vehicle engine telemetry data and provides real-time, explainable engine health insights by learning vehicle-specific baselines instead of using fixed manufacturer thresholds.

---

## ✅ System Architecture Implementation

### 1. Data Ingestion Layer ✅
- **Status:** Implemented and operational
- **Functionality:** Successfully loads telemetry data from `engine_telemetry.csv`
- **Multi-vehicle Support:** System handles multiple vehicles (vehicle_id based grouping)

### 2. Vehicle Profiling Layer ✅
- **Status:** Implemented and operational
- **Functionality:** Stores vehicle metadata (type, engine, cc)
- **Independence:** Each vehicle is treated independently

### 3. Gear-Based Context Modeling ✅
- **Status:** Implemented and operational
- **Functionality:** Segments engine behavior by gear number
- **Learning:** System learns expected behavior per gear instead of global averages

---

## 📊 Live System Output

### API Endpoints Available:
- **Base URL:** http://localhost:8000
- **Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Example 1: Get All Vehicles

**Endpoint:** `GET /vehicles`

**Response:**
```json
{
  "success": true,
  "data": {
    "vehicles": ["VH_01", "VH_02", "VH_03", "VH_04", "VH_05"],
    "count": 5
  }
}
```

**Analysis:**
- System successfully identified **5 vehicles** in the dataset
- All vehicles are properly indexed and accessible

---

### Example 2: Engine Health Status for Vehicle VH_01

**Endpoint:** `GET /engine-status?vehicle_id=VH_01`

**Response:**
```json
{
  "success": true,
  "data": {
    "vehicle_id": "VH_01",
    "timestamp": "2024-01-31T11:04:41",
    "gear": 1,
    
    "current_rpm": 1474.3,
    "current_engine_temp": 75.6,
    "current_oil_pressure": 42.3,
    "current_vibration": 2.55,
    "current_speed_kmph": 23.17,
    
    "rpm_deviation": {
      "current_value": 1474.3,
      "expected_mean": 1503.15,
      "expected_range_min": 1049.17,
      "expected_range_max": 1957.12,
      "deviation_percent": 1.92,
      "deviation_std": 0.13,
      "status": "Normal"
    },
    
    "temp_deviation": {
      "current_value": 75.6,
      "expected_mean": 84.95,
      "expected_range_min": 74.47,
      "expected_range_max": 95.43,
      "deviation_percent": 11.01,
      "deviation_std": 1.78,
      "status": "Normal"
    },
    
    "oil_pressure_deviation": {
      "current_value": 42.3,
      "expected_mean": 45.27,
      "expected_range_min": 36.10,
      "expected_range_max": 54.43,
      "deviation_percent": 6.56,
      "deviation_std": 0.65,
      "status": "Normal"
    },
    
    "vibration_deviation": {
      "current_value": 2.55,
      "expected_mean": 2.53,
      "expected_range_min": 1.44,
      "expected_range_max": 3.61,
      "deviation_percent": 0.87,
      "deviation_std": 0.04,
      "status": "Normal"
    },
    
    "engine_safety_score": 98.16,
    "overall_status": "Normal",
    
    "explanation": "Engine is operating normally for this vehicle in gear 1. All metrics are within expected ranges based on learned baseline behavior. All metrics (RPM, Temperature, Oil Pressure, Vibration) are within expected ranges for this vehicle. Engine Safety Score: 98.2/100 - Healthy operation.",
    
    "recommendations": [
      "Continue normal operation and monitoring."
    ]
  },
  "message": "Engine status retrieved successfully"
}
```

---

## 🎯 Key Features Demonstrated

### ✅ 1. Adaptive Baseline Learning
- **Evidence:** System shows `expected_mean` values that are **learned from data**, not fixed manufacturer specs
- **Example:** VH_01 in gear 1 has:
  - Expected RPM: 1503.15 (learned, not fixed)
  - Expected Temperature: 84.95°C (learned, not fixed)
  - Expected Oil Pressure: 45.27 PSI (learned, not fixed)
  - Expected Vibration: 2.53 (learned, not fixed)

### ✅ 2. Gear-Based Context Modeling
- **Evidence:** System analyzes behavior **per gear** (shown as `"gear": 1`)
- **Functionality:** Each gear has its own learned baseline statistics
- **Benefit:** More accurate detection since engine behavior varies by gear

### ✅ 3. Deviation Detection Without Fixed Thresholds
- **Evidence:** Status determined by:
  - **Standard Deviation Thresholds:** Warning (>2 std), Critical (>3.5 std)
  - **Percentage Thresholds:** Warning (>20%), Critical (>40%)
  - **Adaptive:** Uses the more conservative threshold
- **Example:** RPM deviation of 0.13 std = Normal (not based on fixed "RPM must be 2000" rule)

### ✅ 4. Explainable AI
- **Evidence:** System provides:
  - **Human-readable explanation:** "Engine is operating normally for this vehicle in gear 1..."
  - **Specific deviations:** Shows exact deviation percentages and standard deviations
  - **Actionable recommendations:** "Continue normal operation and monitoring."

### ✅ 5. Engine Safety Score
- **Calculation:** Weighted average of all metrics:
  - Engine Temperature: 30% weight
  - RPM: 25% weight
  - Oil Pressure: 25% weight
  - Vibration: 20% weight
- **Score Interpretation:**
  - **85-100:** Normal operation
  - **60-84:** Warning level
  - **0-59:** Critical risk
- **Example:** VH_01 score = 98.16 (Normal, healthy operation)

---

## 🔬 Technical Implementation Details

### Baseline Learning Process:
1. **Data Segmentation:** Telemetry grouped by `vehicle_id` + `gear`
2. **Statistical Learning:** For each combination, calculates:
   - Mean (expected value)
   - Standard deviation (expected variation)
3. **Minimum Samples:** Requires at least 10 samples before baseline is valid
4. **Dynamic Updates:** Baselines update as new data arrives

### Deviation Detection Logic:
- **No Fixed Limits:** All decisions based on learned patterns
- **Dual Threshold System:**
  - Standard deviation-based (statistical)
  - Percentage-based (relative)
- **Conservative Approach:** Uses stricter threshold for safety

### Risk Scoring Algorithm:
- **Individual Metric Scores:** 0-100 (lower = higher risk)
- **Weighted Combination:** Combines all metrics with importance weights
- **Status Determination:** Based on final Engine Safety Score

---

## 📈 System Capabilities

### ✅ Multi-Vehicle Support
- System successfully handles 5 vehicles (VH_01 through VH_05)
- Each vehicle has independent baselines and analysis

### ✅ Real-Time Analysis
- Fast API response times
- Efficient processing of telemetry data
- Ready for live telemetry streams

### ✅ Power BI Ready
- RESTful API design
- JSON response format
- CORS enabled for web integration
- Comprehensive endpoint documentation

---

## 🎓 Project Requirements Fulfillment

| Requirement | Status | Evidence |
|------------|--------|----------|
| No manufacturer thresholds | ✅ | Uses learned baselines (expected_mean values) |
| Multi-vehicle support | ✅ | 5 vehicles detected and analyzed |
| Gear-based context | ✅ | Analysis per gear (gear: 1 shown) |
| Explainable alerts | ✅ | Human-readable explanations provided |
| Deviation-based detection | ✅ | Status based on std dev and percentage |
| Real-time monitoring | ✅ | Fast API with live data processing |

---

## 🚀 System Status

**✅ ALL SYSTEMS OPERATIONAL**

- Data ingestion: ✅ Working
- Baseline learning: ✅ Working
- Deviation detection: ✅ Working
- Risk scoring: ✅ Working
- Explainable AI: ✅ Working
- REST API: ✅ Working
- Multi-vehicle support: ✅ Working
- Gear-based modeling: ✅ Working

---

**Generated:** 2024-01-31
**API Server:** Running on http://localhost:8000
**Documentation:** Available at http://localhost:8000/docs


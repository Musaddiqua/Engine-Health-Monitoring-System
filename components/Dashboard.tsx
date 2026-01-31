'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import VehicleSelector from './VehicleSelector'
import HealthScoreCard from './HealthScoreCard'
import MetricCard from './MetricCard'
import StatusBadge from './StatusBadge'
import ExplanationCard from './ExplanationCard'

// Use relative API path for Vercel deployment, or env variable for custom backend
const API_URL = typeof window !== 'undefined' 
  ? (process.env.NEXT_PUBLIC_API_URL || (window.location.origin.includes('vercel.app') ? '/api' : 'http://localhost:8000'))
  : process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface EngineStatus {
  vehicle_id: string
  timestamp: string
  gear: number
  current_rpm: number
  current_engine_temp: number
  current_oil_pressure: number
  current_vibration: number
  current_speed_kmph: number
  rpm_deviation: any
  temp_deviation: any
  oil_pressure_deviation: any
  vibration_deviation: any
  engine_safety_score: number
  overall_status: string
  explanation: string
  recommendations: string[]
}

export default function Dashboard() {
  const [vehicles, setVehicles] = useState<string[]>([])
  const [selectedVehicle, setSelectedVehicle] = useState<string>('')
  const [engineStatus, setEngineStatus] = useState<EngineStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchVehicles()
  }, [])

  useEffect(() => {
    if (selectedVehicle) {
      fetchEngineStatus(selectedVehicle)
      // Auto-refresh every 5 seconds
      const interval = setInterval(() => {
        fetchEngineStatus(selectedVehicle)
      }, 5000)
      return () => clearInterval(interval)
    }
  }, [selectedVehicle])

  const fetchVehicles = async () => {
    try {
      const response = await axios.get(`${API_URL}/vehicles`)
      const vehicleList = response.data.data?.vehicles || []
      setVehicles(vehicleList)
      if (vehicleList.length > 0 && !selectedVehicle) {
        setSelectedVehicle(vehicleList[0])
      }
    } catch (err: any) {
      setError('Failed to fetch vehicles. Make sure the API server is running.')
      console.error('Error fetching vehicles:', err)
    }
  }

  const fetchEngineStatus = async (vehicleId: string) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_URL}/engine-status`, {
        params: { vehicle_id: vehicleId }
      })
      if (response.data.success && response.data.data) {
        setEngineStatus(response.data.data)
      } else {
        setError(response.data.message || 'Failed to fetch engine status')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch engine status')
      console.error('Error fetching engine status:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'normal':
        return 'bg-green-100 text-green-800 border-green-300'
      case 'warning':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                🚗 Engine Health Monitoring System
              </h1>
              <p className="text-gray-600">
                AI-Powered Adaptive Baseline Learning • Real-Time Insights
              </p>
            </div>
            <div className="flex items-center gap-4">
              {engineStatus && (
                <StatusBadge 
                  status={engineStatus.overall_status}
                  className="text-lg px-4 py-2"
                />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Vehicle Selector */}
      <div className="max-w-7xl mx-auto mb-6">
        <VehicleSelector
          vehicles={vehicles}
          selectedVehicle={selectedVehicle}
          onSelect={setSelectedVehicle}
          loading={loading}
        />
      </div>

      {error && (
        <div className="max-w-7xl mx-auto mb-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
            ⚠️ {error}
          </div>
        </div>
      )}

      {engineStatus && (
        <div className="max-w-7xl mx-auto">
          {/* Health Score Card */}
          <div className="mb-6">
            <HealthScoreCard
              score={engineStatus.engine_safety_score}
              status={engineStatus.overall_status}
              vehicleId={engineStatus.vehicle_id}
              gear={engineStatus.gear}
              timestamp={engineStatus.timestamp}
            />
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <MetricCard
              title="RPM"
              current={engineStatus.current_rpm}
              expected={engineStatus.rpm_deviation.expected_mean}
              deviation={engineStatus.rpm_deviation}
              unit="rpm"
              icon="⚡"
            />
            <MetricCard
              title="Engine Temperature"
              current={engineStatus.current_engine_temp}
              expected={engineStatus.temp_deviation.expected_mean}
              deviation={engineStatus.temp_deviation}
              unit="°C"
              icon="🌡️"
            />
            <MetricCard
              title="Oil Pressure"
              current={engineStatus.current_oil_pressure}
              expected={engineStatus.oil_pressure_deviation.expected_mean}
              deviation={engineStatus.oil_pressure_deviation}
              unit="PSI"
              icon="🛢️"
            />
            <MetricCard
              title="Vibration"
              current={engineStatus.current_vibration}
              expected={engineStatus.vibration_deviation.expected_mean}
              deviation={engineStatus.vibration_deviation}
              unit=""
              icon="📳"
            />
          </div>

          {/* Explanation and Recommendations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ExplanationCard
              explanation={engineStatus.explanation}
              recommendations={engineStatus.recommendations}
            />
            
            {/* Additional Info Card */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                📊 Current Status
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Speed:</span>
                  <span className="font-semibold text-gray-900">
                    {engineStatus.current_speed_kmph.toFixed(1)} km/h
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Gear:</span>
                  <span className="font-semibold text-gray-900">
                    {engineStatus.gear}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Vehicle ID:</span>
                  <span className="font-semibold text-gray-900">
                    {engineStatus.vehicle_id}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Last Updated:</span>
                  <span className="font-semibold text-gray-900 text-sm">
                    {new Date(engineStatus.timestamp).toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {!engineStatus && !loading && !error && (
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-12 text-center border border-gray-200">
            <p className="text-gray-500 text-lg">
              Select a vehicle to view engine health status
            </p>
          </div>
        </div>
      )}
    </div>
  )
}


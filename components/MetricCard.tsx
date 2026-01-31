'use client'

import StatusBadge from './StatusBadge'

interface MetricCardProps {
  title: string
  current: number
  expected: number
  deviation: any
  unit: string
  icon: string
}

export default function MetricCard({
  title,
  current,
  expected,
  deviation,
  unit,
  icon
}: MetricCardProps) {
  const deviationPercent = deviation.deviation_percent
  const isWithinRange = deviation.status === 'Normal'
  
  const getBarColor = () => {
    if (deviation.status === 'Critical') return 'bg-red-500'
    if (deviation.status === 'Warning') return 'bg-yellow-500'
    return 'bg-green-500'
  }

  const percentage = Math.min(Math.abs(deviationPercent), 100)

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200 hover:shadow-xl transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <span className="text-2xl">{icon}</span>
          {title}
        </h3>
        <StatusBadge status={deviation.status} />
      </div>

      <div className="space-y-4">
        <div>
          <div className="flex justify-between items-baseline mb-2">
            <span className="text-3xl font-bold text-gray-900">
              {current.toFixed(1)}
            </span>
            <span className="text-gray-500 text-sm">{unit}</span>
          </div>
          <div className="text-sm text-gray-600">
            Expected: <span className="font-medium">{expected.toFixed(1)} {unit}</span>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs text-gray-600 mb-1">
            <span>Deviation</span>
            <span className="font-semibold">{deviationPercent.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${getBarColor()}`}
              style={{ width: `${Math.min(percentage, 100)}%` }}
            />
          </div>
        </div>

        <div className="pt-2 border-t border-gray-100">
          <div className="flex justify-between text-xs text-gray-500">
            <span>Range:</span>
            <span>
              {deviation.expected_range_min.toFixed(1)} - {deviation.expected_range_max.toFixed(1)} {unit}
            </span>
          </div>
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Std Dev:</span>
            <span className="font-medium">{deviation.deviation_std.toFixed(2)}σ</span>
          </div>
        </div>
      </div>
    </div>
  )
}



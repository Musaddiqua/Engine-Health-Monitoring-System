'use client'

import StatusBadge from './StatusBadge'

interface HealthScoreCardProps {
  score: number
  status: string
  vehicleId: string
  gear: number
  timestamp: string
}

export default function HealthScoreCard({
  score,
  status,
  vehicleId,
  gear,
  timestamp
}: HealthScoreCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 85) return 'bg-green-50 border-green-200'
    if (score >= 60) return 'bg-yellow-50 border-yellow-200'
    return 'bg-red-50 border-red-200'
  }

  const circumference = 2 * Math.PI * 90
  const offset = circumference - (score / 100) * circumference

  return (
    <div className={`bg-white rounded-xl shadow-lg p-8 border-2 ${getScoreBgColor(score)}`}>
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Score Circle */}
        <div className="relative w-48 h-48 flex-shrink-0">
          <svg className="transform -rotate-90 w-48 h-48">
            <circle
              cx="96"
              cy="96"
              r="90"
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              className="text-gray-200"
            />
            <circle
              cx="96"
              cy="96"
              r="90"
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              className={`transition-all duration-1000 ${getScoreColor(score)}`}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className={`text-5xl font-bold ${getScoreColor(score)}`}>
              {score.toFixed(1)}
            </div>
            <div className="text-gray-600 text-sm mt-1">/ 100</div>
          </div>
        </div>

        {/* Info Section */}
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Engine Safety Score
          </h2>
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-gray-600 w-32">Status:</span>
              <StatusBadge status={status} />
            </div>
            <div className="flex items-center gap-3">
              <span className="text-gray-600 w-32">Vehicle:</span>
              <span className="font-semibold text-gray-900">{vehicleId}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-gray-600 w-32">Gear:</span>
              <span className="font-semibold text-gray-900">{gear}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-gray-600 w-32">Updated:</span>
              <span className="text-sm text-gray-700">
                {new Date(timestamp).toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}



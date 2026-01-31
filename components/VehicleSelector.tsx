'use client'

interface VehicleSelectorProps {
  vehicles: string[]
  selectedVehicle: string
  onSelect: (vehicleId: string) => void
  loading: boolean
}

export default function VehicleSelector({
  vehicles,
  selectedVehicle,
  onSelect,
  loading
}: VehicleSelectorProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Select Vehicle
      </h2>
      <div className="flex flex-wrap gap-3">
        {vehicles.map((vehicle) => (
          <button
            key={vehicle}
            onClick={() => onSelect(vehicle)}
            disabled={loading}
            className={`
              px-6 py-3 rounded-lg font-medium transition-all duration-200
              ${
                selectedVehicle === vehicle
                  ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }
              ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            {vehicle}
          </button>
        ))}
      </div>
    </div>
  )
}



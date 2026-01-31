'use client'

import { useState, useEffect } from 'react'
import Dashboard from '@/components/Dashboard'
import LoadingSpinner from '@/components/LoadingSpinner'

export default function Home() {
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate initial load
    setTimeout(() => setLoading(false), 500)
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100">
      <Dashboard />
    </main>
  )
}



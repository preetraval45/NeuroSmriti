'use client'

import React, { useState, useEffect } from 'react'

interface SafeZone {
  zone_id: string
  name: string
  center: { latitude: number; longitude: number }
  radius_meters: number
  enabled: boolean
}

interface Location {
  latitude: number
  longitude: number
  timestamp: string
}

export default function GPSTracker({ patientId }: { patientId: number }) {
  const [currentLocation, setCurrentLocation] = useState<Location | null>(null)
  const [safeZones, setSafeZones] = useState<SafeZone[]>([])
  const [insideSafeZone, setInsideSafeZone] = useState(true)
  const [isTracking, setIsTracking] = useState(false)
  const [showAddZone, setShowAddZone] = useState(false)
  const [newZone, setNewZone] = useState({
    name: '',
    radius_meters: 500
  })

  useEffect(() => {
    fetchSafeZones()
  }, [patientId])

  useEffect(() => {
    if (isTracking) {
      const watchId = navigator.geolocation.watchPosition(
        (position) => {
          const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            timestamp: new Date().toISOString()
          }
          setCurrentLocation(location)
          checkLocation(location)
        },
        (error) => {
          console.error('Location tracking error:', error)
        },
        {
          enableHighAccuracy: true,
          maximumAge: 10000,
          timeout: 5000
        }
      )

      return () => navigator.geolocation.clearWatch(watchId)
    }
  }, [isTracking])

  const fetchSafeZones = async () => {
    try {
      const response = await fetch(`/api/v1/safety/gps/safe-zones/${patientId}`)
      if (response.ok) {
        const data = await response.json()
        setSafeZones(data.safe_zones || [])
      }
    } catch (error) {
      console.error('Error fetching safe zones:', error)
    }
  }

  const checkLocation = async (location: Location) => {
    try {
      const response = await fetch('/api/v1/safety/gps/check-location', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: patientId,
          latitude: location.latitude,
          longitude: location.longitude,
          timestamp: location.timestamp
        })
      })

      if (response.ok) {
        const result = await response.json()
        setInsideSafeZone(result.inside_safe_zone)

        if (result.alert_triggered) {
          // Show notification
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Wandering Alert', {
              body: 'Patient has left the safe zone!',
              icon: '/alert-icon.png',
              tag: 'wandering-alert'
            })
          }
        }
      }
    } catch (error) {
      console.error('Error checking location:', error)
    }
  }

  const createSafeZone = async () => {
    if (!currentLocation || !newZone.name) {
      alert('Please enable location and enter a zone name')
      return
    }

    try {
      const response = await fetch('/api/v1/safety/gps/create-safe-zone', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: patientId,
          zone_name: newZone.name,
          center_lat: currentLocation.latitude,
          center_lon: currentLocation.longitude,
          radius_meters: newZone.radius_meters,
          active_times: [{ start: '00:00', end: '23:59' }]
        })
      })

      if (response.ok) {
        setShowAddZone(false)
        setNewZone({ name: '', radius_meters: 500 })
        fetchSafeZones()
        alert('Safe zone created successfully!')
      }
    } catch (error) {
      console.error('Error creating safe zone:', error)
      alert('Error creating safe zone')
    }
  }

  const requestNotificationPermission = async () => {
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission()
    }
  }

  const startTracking = () => {
    setIsTracking(true)
    requestNotificationPermission()
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
          <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          GPS Tracking
        </h2>
        <button
          onClick={() => setIsTracking(!isTracking)}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            isTracking
              ? 'bg-red-600 hover:bg-red-700 text-white'
              : 'bg-green-600 hover:bg-green-700 text-white'
          }`}
        >
          {isTracking ? 'Stop Tracking' : 'Start Tracking'}
        </button>
      </div>

      {/* Current Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className={`p-4 rounded-lg border-2 ${
          insideSafeZone ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
        }`}>
          <div className="flex items-center">
            {insideSafeZone ? (
              <svg className="w-8 h-8 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : (
              <svg className="w-8 h-8 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            )}
            <div>
              <p className="text-sm font-semibold text-gray-700">Status</p>
              <p className={`text-lg font-bold ${insideSafeZone ? 'text-green-600' : 'text-red-600'}`}>
                {insideSafeZone ? 'Inside Safe Zone' : 'Outside Safe Zone'}
              </p>
            </div>
          </div>
        </div>

        <div className="p-4 bg-blue-50 border-2 border-blue-200 rounded-lg">
          <div className="flex items-center">
            <svg className="w-8 h-8 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="text-sm font-semibold text-gray-700">Tracking</p>
              <p className="text-lg font-bold text-blue-600">
                {isTracking ? 'Active' : 'Inactive'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Current Location */}
      {currentLocation && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-700 mb-2">Current Location</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-600">Latitude</p>
              <p className="font-mono text-gray-900">{currentLocation.latitude.toFixed(6)}</p>
            </div>
            <div>
              <p className="text-gray-600">Longitude</p>
              <p className="font-mono text-gray-900">{currentLocation.longitude.toFixed(6)}</p>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Last updated: {new Date(currentLocation.timestamp).toLocaleString()}
          </p>
        </div>
      )}

      {/* Safe Zones */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-700">Safe Zones ({safeZones.length})</h3>
          <button
            onClick={() => setShowAddZone(!showAddZone)}
            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition"
          >
            + Add Zone
          </button>
        </div>

        {showAddZone && (
          <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-semibold text-gray-700 mb-3">Create New Safe Zone</h4>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Zone Name</label>
                <input
                  type="text"
                  value={newZone.name}
                  onChange={(e) => setNewZone({ ...newZone, name: e.target.value })}
                  placeholder="e.g., Home, Park"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Radius: {newZone.radius_meters}m
                </label>
                <input
                  type="range"
                  min="100"
                  max="2000"
                  step="100"
                  value={newZone.radius_meters}
                  onChange={(e) => setNewZone({ ...newZone, radius_meters: parseInt(e.target.value) })}
                  className="w-full"
                />
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={createSafeZone}
                  className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition"
                >
                  Create
                </button>
                <button
                  onClick={() => setShowAddZone(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-lg transition"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-2">
          {safeZones.length === 0 ? (
            <p className="text-gray-500 text-sm text-center py-4">No safe zones configured</p>
          ) : (
            safeZones.map((zone) => (
              <div key={zone.zone_id} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-900">{zone.name}</p>
                    <p className="text-sm text-gray-600">
                      Radius: {zone.radius_meters}m • {zone.enabled ? 'Active' : 'Inactive'}
                    </p>
                  </div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Info */}
      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <div className="flex">
          <svg className="w-5 h-5 text-yellow-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div className="text-sm text-yellow-800">
            <p className="font-semibold mb-1">How GPS Tracking Works:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Create safe zones around familiar locations</li>
              <li>Receive alerts if patient leaves safe zones</li>
              <li>Track location history for peace of mind</li>
              <li>Battery-efficient background tracking</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

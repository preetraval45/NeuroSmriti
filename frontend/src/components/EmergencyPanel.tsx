'use client'

import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface EmergencyContact {
  name: string
  phone: string
  relationship: string
  priority: number
}

interface Location {
  latitude: number
  longitude: number
}

export default function EmergencyPanel() {
  const router = useRouter()
  const [isExpanded, setIsExpanded] = useState(false)
  const [emergencyContacts, setEmergencyContacts] = useState<EmergencyContact[]>([])
  const [currentLocation, setCurrentLocation] = useState<Location | null>(null)
  const [alertInProgress, setAlertInProgress] = useState(false)

  // Get current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCurrentLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          })
        },
        (error) => {
          console.error('Location access denied:', error)
        }
      )
    }
  }, [])

  const triggerEmergencyAlert = async (alertType: string) => {
    setAlertInProgress(true)

    try {
      const response = await fetch('/api/v1/communication/emergency/trigger-alert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: 1, // Would come from auth context
          alert_type: alertType,
          location: currentLocation,
          message: `Emergency alert: ${alertType}`
        })
      })

      if (response.ok) {
        const result = await response.json()
        alert(`Emergency contacts notified! Alert ID: ${result.alert_id}`)
      } else {
        alert('Failed to send emergency alert')
      }
    } catch (error) {
      console.error('Error sending emergency alert:', error)
      alert('Error sending emergency alert')
    } finally {
      setAlertInProgress(false)
    }
  }

  const EmergencyButton = ({
    icon,
    label,
    color,
    alertType
  }: {
    icon: React.ReactNode
    label: string
    color: string
    alertType: string
  }) => (
    <button
      onClick={() => triggerEmergencyAlert(alertType)}
      disabled={alertInProgress}
      className={`flex flex-col items-center justify-center p-4 rounded-lg ${color} text-white transition transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      <div className="w-12 h-12 mb-2">{icon}</div>
      <span className="text-sm font-medium">{label}</span>
    </button>
  )

  if (!isExpanded) {
    return (
      <div className="fixed bottom-32 right-6 z-40 no-print">
        <button
          onClick={() => setIsExpanded(true)}
          className="w-14 h-14 rounded-full bg-red-600 hover:bg-red-700 shadow-lg flex items-center justify-center text-white transition transform hover:scale-110"
          aria-label="Emergency options"
        >
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </button>
      </div>
    )
  }

  return (
    <div className="fixed bottom-32 right-6 z-40 bg-white rounded-lg shadow-2xl p-6 w-80 no-print">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-900 flex items-center">
          <svg className="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          Emergency
        </h3>
        <button
          onClick={() => setIsExpanded(false)}
          className="text-gray-400 hover:text-gray-600"
          aria-label="Close emergency panel"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Emergency Buttons Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <EmergencyButton
          icon={
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          }
          label="Call 911"
          color="bg-red-600 hover:bg-red-700"
          alertType="medical"
        />

        <EmergencyButton
          icon={
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          }
          label="Lost/Wandering"
          color="bg-orange-600 hover:bg-orange-700"
          alertType="wandering"
        />

        <EmergencyButton
          icon={
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          }
          label="Fall Detected"
          color="bg-yellow-600 hover:bg-yellow-700"
          alertType="fall"
        />

        <EmergencyButton
          icon={
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          }
          label="Panic Button"
          color="bg-purple-600 hover:bg-purple-700"
          alertType="panic_button"
        />
      </div>

      {/* Location Status */}
      {currentLocation && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-xs text-green-800 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Location enabled
          </p>
        </div>
      )}

      {/* Quick Actions */}
      <div className="space-y-2">
        <button
          onClick={() => router.push('/emergency-contacts')}
          className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition"
        >
          📞 Manage Emergency Contacts
        </button>
        <button
          onClick={() => router.push('/safety-settings')}
          className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition"
        >
          ⚙️ Safety Settings
        </button>
        <button
          onClick={() => router.push('/safety/alert-history')}
          className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition"
        >
          📋 Alert History
        </button>
      </div>

      {/* Disclaimer */}
      <p className="mt-4 text-xs text-gray-500 text-center">
        In life-threatening emergencies, call 911 immediately
      </p>
    </div>
  )
}

'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function DigitalBiomarkersPage() {
  const [connected, setConnected] = useState(false)
  const [connecting, setConnecting] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedDevice, setSelectedDevice] = useState<string | null>(null)

  const devices = [
    { id: 'smartphone', name: 'Smartphone', icon: '📱', connected: true },
    { id: 'smartwatch', name: 'Smartwatch', icon: '⌚', connected: false },
    { id: 'tablet', name: 'Tablet', icon: '📲', connected: false },
    { id: 'fitness', name: 'Fitness Tracker', icon: '💪', connected: false }
  ]

  const biomarkers = [
    {
      category: 'Motor Function',
      metrics: [
        { name: 'Typing Speed', value: 45, unit: 'WPM', trend: 'stable', baseline: 48 },
        { name: 'Keystroke Dynamics', value: 82, unit: '%', trend: 'down', baseline: 88 },
        { name: 'Touch Accuracy', value: 91, unit: '%', trend: 'stable', baseline: 92 },
        { name: 'Swipe Patterns', value: 78, unit: 'score', trend: 'stable', baseline: 80 }
      ]
    },
    {
      category: 'Cognitive Patterns',
      metrics: [
        { name: 'App Usage Consistency', value: 73, unit: '%', trend: 'down', baseline: 85 },
        { name: 'Task Completion', value: 88, unit: '%', trend: 'stable', baseline: 90 },
        { name: 'Navigation Efficiency', value: 76, unit: 'score', trend: 'down', baseline: 82 },
        { name: 'Response Time', value: 420, unit: 'ms', trend: 'up', baseline: 380 }
      ]
    },
    {
      category: 'Daily Activity',
      metrics: [
        { name: 'Sleep Quality', value: 72, unit: '%', trend: 'down', baseline: 78 },
        { name: 'Physical Activity', value: 6500, unit: 'steps', trend: 'stable', baseline: 7000 },
        { name: 'Social Interactions', value: 12, unit: '/day', trend: 'down', baseline: 18 },
        { name: 'Screen Time', value: 4.2, unit: 'hrs', trend: 'up', baseline: 3.5 }
      ]
    }
  ]

  const connectDevice = () => {
    if (!selectedDevice) return
    setConnecting(true)
    setTimeout(() => {
      setConnecting(false)
      setConnected(true)
      analyzeBiomarkers()
    }, 2000)
  }

  const analyzeBiomarkers = () => {
    setAnalyzing(true)
    setTimeout(() => {
      setAnalyzing(false)
      setResults({
        overallScore: 76,
        riskLevel: 'low',
        summary: 'Digital biomarker analysis shows mostly normal patterns with some areas to monitor.',
        changes: [
          { marker: 'App Usage Patterns', change: -12, significance: 'moderate' },
          { marker: 'Social Engagement', change: -33, significance: 'notable' },
          { marker: 'Sleep Regularity', change: -8, significance: 'mild' },
          { marker: 'Motor Function', change: -5, significance: 'minimal' }
        ],
        recommendations: [
          'Maintain regular sleep schedule',
          'Increase social interactions and communications',
          'Consider cognitive exercise apps',
          'Schedule follow-up assessment in 30 days'
        ]
      })
    }, 3000)
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '↑'
      case 'down': return '↓'
      default: return '→'
    }
  }

  const getTrendColor = (trend: string, metric: string) => {
    // For some metrics, up is bad (like response time, screen time)
    const inverseMetrics = ['Response Time', 'Screen Time']
    const isInverse = inverseMetrics.includes(metric)

    if (trend === 'stable') return 'text-gray-500'
    if (trend === 'up') return isInverse ? 'text-red-500' : 'text-green-500'
    if (trend === 'down') return isInverse ? 'text-green-500' : 'text-red-500'
    return 'text-gray-500'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-pink-500 to-rose-500 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Link href="/detection" className="inline-flex items-center text-pink-100 hover:text-white mb-4">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Detection
            </Link>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Digital Biomarkers</h1>
            <p className="text-xl text-pink-100">
              Continuous monitoring through everyday device usage patterns
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-5xl mx-auto">
          {!connected && (
            <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
              <div className="text-center mb-8">
                <div className="w-20 h-20 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-4xl">📱</span>
                </div>
                <h2 className="text-2xl font-bold mb-2">Connect Your Devices</h2>
                <p className="text-gray-600 max-w-lg mx-auto">
                  Connect your devices to enable continuous monitoring of digital biomarkers
                  that can indicate early cognitive changes.
                </p>
              </div>

              {/* Device Selection */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                {devices.map(device => (
                  <button
                    key={device.id}
                    type="button"
                    onClick={() => setSelectedDevice(device.id)}
                    className={`p-6 rounded-xl border-2 transition text-center ${
                      selectedDevice === device.id
                        ? 'border-pink-500 bg-pink-50'
                        : 'border-gray-200 hover:border-pink-300'
                    }`}
                  >
                    <span className="text-4xl block mb-2">{device.icon}</span>
                    <span className="font-medium">{device.name}</span>
                  </button>
                ))}
              </div>

              {/* What We Track */}
              <div className="bg-gray-50 rounded-xl p-6 mb-8">
                <h3 className="font-semibold mb-4">What We Monitor:</h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="flex items-start">
                    <span className="text-pink-500 mr-2">✓</span>
                    <div>
                      <p className="font-medium">Typing Patterns</p>
                      <p className="text-sm text-gray-600">Speed, accuracy, rhythm</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <span className="text-pink-500 mr-2">✓</span>
                    <div>
                      <p className="font-medium">App Usage</p>
                      <p className="text-sm text-gray-600">Frequency, duration, patterns</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <span className="text-pink-500 mr-2">✓</span>
                    <div>
                      <p className="font-medium">Social Interactions</p>
                      <p className="text-sm text-gray-600">Calls, messages, contacts</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <span className="text-pink-500 mr-2">✓</span>
                    <div>
                      <p className="font-medium">Sleep Patterns</p>
                      <p className="text-sm text-gray-600">Duration, quality, schedule</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <span className="text-pink-500 mr-2">✓</span>
                    <div>
                      <p className="font-medium">Physical Activity</p>
                      <p className="text-sm text-gray-600">Steps, movement, exercise</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <span className="text-pink-500 mr-2">✓</span>
                    <div>
                      <p className="font-medium">Navigation</p>
                      <p className="text-sm text-gray-600">GPS patterns, locations</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-center">
                <button
                  type="button"
                  onClick={connectDevice}
                  disabled={!selectedDevice || connecting}
                  className="px-8 py-4 bg-pink-500 text-white rounded-xl font-semibold hover:bg-pink-600 transition disabled:opacity-50"
                >
                  {connecting ? (
                    <span className="flex items-center">
                      <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Connecting...
                    </span>
                  ) : (
                    'Connect Device'
                  )}
                </button>
                <p className="text-sm text-gray-500 mt-4">
                  Your data is encrypted and only used for health analysis
                </p>
              </div>
            </div>
          )}

          {connected && analyzing && (
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
              <div className="w-20 h-20 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="animate-spin h-10 w-10 text-pink-500" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold mb-2">Analyzing Digital Biomarkers</h2>
              <p className="text-gray-600">Processing usage patterns and behavioral data...</p>
            </div>
          )}

          {connected && results && (
            <>
              {/* Overall Score */}
              <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold">Digital Biomarker Analysis</h2>
                    <p className="text-gray-600">Based on 30 days of usage data</p>
                  </div>
                  <div className="text-right">
                    <p className="text-4xl font-bold text-pink-600">{results.overallScore}/100</p>
                    <p className={`font-semibold ${
                      results.riskLevel === 'low' ? 'text-green-600' :
                      results.riskLevel === 'moderate' ? 'text-yellow-600' :
                      'text-red-600'
                    }`}>
                      {results.riskLevel.charAt(0).toUpperCase() + results.riskLevel.slice(1)} Risk
                    </p>
                  </div>
                </div>
                <p className="text-gray-700 bg-gray-50 rounded-xl p-4">{results.summary}</p>
              </div>

              {/* Biomarker Categories */}
              {biomarkers.map((category, catIndex) => (
                <div key={catIndex} className="bg-white rounded-2xl shadow-lg p-8 mb-8">
                  <h3 className="text-xl font-bold mb-6">{category.category}</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {category.metrics.map((metric, i) => (
                      <div key={i} className="bg-gray-50 rounded-xl p-4">
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-medium">{metric.name}</span>
                          <span className={`flex items-center ${getTrendColor(metric.trend, metric.name)}`}>
                            {getTrendIcon(metric.trend)}
                            <span className="ml-1 text-sm">{metric.trend}</span>
                          </span>
                        </div>
                        <div className="flex items-end justify-between">
                          <div>
                            <span className="text-2xl font-bold">{metric.value}</span>
                            <span className="text-gray-500 ml-1">{metric.unit}</span>
                          </div>
                          <div className="text-sm text-gray-500">
                            Baseline: {metric.baseline} {metric.unit}
                          </div>
                        </div>
                        <div className="mt-2 h-2 bg-gray-200 rounded-full">
                          <div
                            className="h-full bg-pink-500 rounded-full"
                            style={{
                              width: `${Math.min(100, (metric.value / metric.baseline) * 100)}%`
                            }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}

              {/* Changes Detected */}
              <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
                <h3 className="text-xl font-bold mb-6">Notable Changes</h3>
                <div className="space-y-4">
                  {results.changes.map((change: any, i: number) => (
                    <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div>
                        <p className="font-medium">{change.marker}</p>
                        <p className={`text-sm ${
                          change.significance === 'notable' ? 'text-red-500' :
                          change.significance === 'moderate' ? 'text-yellow-500' :
                          'text-gray-500'
                        }`}>
                          {change.significance.charAt(0).toUpperCase() + change.significance.slice(1)} change
                        </p>
                      </div>
                      <div className={`text-xl font-bold ${change.change < 0 ? 'text-red-500' : 'text-green-500'}`}>
                        {change.change > 0 ? '+' : ''}{change.change}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div className="bg-gradient-to-r from-pink-50 to-rose-50 rounded-2xl p-8 mb-8">
                <h3 className="text-xl font-bold mb-4">Recommendations</h3>
                <ul className="space-y-3">
                  {results.recommendations.map((rec: string, i: number) => (
                    <li key={i} className="flex items-start">
                      <span className="w-6 h-6 bg-pink-500 text-white rounded-full flex items-center justify-center text-sm mr-3 flex-shrink-0">
                        {i + 1}
                      </span>
                      <span className="text-gray-700">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Actions */}
              <div className="flex justify-between">
                <Link
                  href="/detection"
                  className="px-6 py-3 border-2 border-gray-300 text-gray-600 rounded-xl font-semibold hover:bg-gray-50 transition"
                >
                  Back to Detection
                </Link>
                <Link
                  href="/dashboard"
                  className="px-6 py-3 bg-pink-500 text-white rounded-xl font-semibold hover:bg-pink-600 transition"
                >
                  View Full Dashboard
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

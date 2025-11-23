'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'

export default function EyeTrackingPage() {
  const [testStarted, setTestStarted] = useState(false)
  const [currentTest, setCurrentTest] = useState(0)
  const [testComplete, setTestComplete] = useState(false)
  const [calibrating, setCalibrating] = useState(false)
  const [calibrated, setCalibrated] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [gazePoint, setGazePoint] = useState({ x: 50, y: 50 })
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const eyeTests = [
    {
      id: 1,
      name: 'Smooth Pursuit',
      description: 'Follow the moving dot with your eyes',
      duration: 15
    },
    {
      id: 2,
      name: 'Saccade Test',
      description: 'Look quickly between the appearing dots',
      duration: 20
    },
    {
      id: 3,
      name: 'Reading Pattern',
      description: 'Read the text naturally while we track your eye movements',
      duration: 30
    },
    {
      id: 4,
      name: 'Visual Search',
      description: 'Find the target objects among distractors',
      duration: 25
    }
  ]

  const startCalibration = () => {
    setCalibrating(true)
    // Simulate calibration
    setTimeout(() => {
      setCalibrating(false)
      setCalibrated(true)
    }, 3000)
  }

  const startTest = () => {
    setTestStarted(true)
    runTest()
  }

  const runTest = () => {
    // Simulate eye tracking with random movement
    const interval = setInterval(() => {
      setGazePoint({
        x: 30 + Math.random() * 40,
        y: 30 + Math.random() * 40
      })
    }, 100)

    setTimeout(() => {
      clearInterval(interval)
      if (currentTest < eyeTests.length - 1) {
        setCurrentTest(prev => prev + 1)
        runTest()
      } else {
        setTestComplete(true)
        generateResults()
      }
    }, eyeTests[currentTest].duration * 1000 / 4) // Shortened for demo
  }

  const generateResults = () => {
    setResults({
      overallScore: 81,
      metrics: {
        smoothPursuit: {
          score: 85,
          status: 'Normal',
          details: 'Eye movement follows targets smoothly with minimal lag'
        },
        saccades: {
          score: 78,
          status: 'Slightly Reduced',
          details: 'Minor delay in rapid eye movements between targets'
        },
        fixation: {
          score: 82,
          status: 'Normal',
          details: 'Stable fixation with appropriate duration'
        },
        readingPattern: {
          score: 79,
          status: 'Normal',
          details: 'Left-to-right pattern maintained, slight regression noted'
        }
      },
      observations: [
        'Smooth pursuit accuracy is within normal limits',
        'Saccadic movements show slight latency increase',
        'Reading patterns are consistent with age norms',
        'Visual attention span is adequate'
      ],
      cognitiveIndicators: {
        attention: 'Normal',
        processing: 'Slightly Reduced',
        memory: 'Normal',
        executive: 'Normal'
      }
    })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-orange-500 to-amber-500 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Link href="/detection" className="inline-flex items-center text-orange-100 hover:text-white mb-4">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Detection
            </Link>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Eye Tracking Analysis</h1>
            <p className="text-xl text-orange-100">
              Monitor eye movements and patterns to detect early cognitive changes
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {!testStarted && !testComplete && (
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="text-center mb-8">
                <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-4xl">👁️</span>
                </div>
                <h2 className="text-2xl font-bold mb-2">Eye Tracking Assessment</h2>
                <p className="text-gray-600">
                  This test uses your device camera to track eye movements and analyze cognitive patterns.
                </p>
              </div>

              {/* Test Overview */}
              <div className="grid md:grid-cols-2 gap-4 mb-8">
                {eyeTests.map((test, i) => (
                  <div key={test.id} className="bg-gray-50 rounded-xl p-4">
                    <div className="flex items-center mb-2">
                      <span className="w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">
                        {i + 1}
                      </span>
                      <h3 className="font-semibold">{test.name}</h3>
                    </div>
                    <p className="text-sm text-gray-600 ml-11">{test.description}</p>
                  </div>
                ))}
              </div>

              {/* Calibration */}
              {!calibrated ? (
                <div className="text-center">
                  <div className="bg-orange-50 rounded-xl p-6 mb-6">
                    <h3 className="font-semibold mb-2">Before we begin:</h3>
                    <ul className="text-left text-gray-600 space-y-2 max-w-md mx-auto">
                      <li>• Ensure good lighting on your face</li>
                      <li>• Position yourself at arm&apos;s length from the screen</li>
                      <li>• Keep your head still during the test</li>
                      <li>• Remove glasses if they cause reflections</li>
                    </ul>
                  </div>
                  <button
                    type="button"
                    onClick={startCalibration}
                    disabled={calibrating}
                    className="px-8 py-4 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition disabled:opacity-50"
                  >
                    {calibrating ? (
                      <span className="flex items-center">
                        <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Calibrating Camera...
                      </span>
                    ) : (
                      'Start Calibration'
                    )}
                  </button>
                </div>
              ) : (
                <div className="text-center">
                  <div className="flex items-center justify-center text-green-600 mb-6">
                    <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="font-semibold">Calibration Complete!</span>
                  </div>
                  <button
                    type="button"
                    onClick={startTest}
                    className="px-8 py-4 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition"
                  >
                    Begin Eye Tracking Test
                  </button>
                </div>
              )}
            </div>
          )}

          {testStarted && !testComplete && (
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="mb-6">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Test {currentTest + 1} of {eyeTests.length}: {eyeTests[currentTest].name}</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full">
                  <div
                    className="h-full bg-orange-500 rounded-full transition-all"
                    style={{ width: `${((currentTest + 1) / eyeTests.length) * 100}%` }}
                  />
                </div>
              </div>

              {/* Test Area */}
              <div className="relative bg-gray-900 rounded-xl h-96 mb-4 overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center">
                  <p className="text-white text-xl">{eyeTests[currentTest].description}</p>
                </div>
                {/* Simulated gaze point */}
                <div
                  className="absolute w-4 h-4 bg-orange-500 rounded-full transition-all duration-100"
                  style={{
                    left: `${gazePoint.x}%`,
                    top: `${gazePoint.y}%`,
                    transform: 'translate(-50%, -50%)'
                  }}
                />
                {/* Target point */}
                <div
                  className="absolute w-6 h-6 bg-white rounded-full animate-pulse"
                  style={{
                    left: `${50 + Math.sin(Date.now() / 1000) * 30}%`,
                    top: `${50 + Math.cos(Date.now() / 1000) * 20}%`,
                    transform: 'translate(-50%, -50%)'
                  }}
                />
              </div>

              <p className="text-center text-gray-600">
                Keep your eyes on the white dot and follow its movement
              </p>
            </div>
          )}

          {testComplete && results && (
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="text-center mb-8">
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-4xl">✅</span>
                </div>
                <h2 className="text-2xl font-bold mb-2">Assessment Complete</h2>
              </div>

              {/* Overall Score */}
              <div className="bg-gradient-to-r from-orange-50 to-amber-50 rounded-xl p-6 mb-8">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600">Eye Tracking Score</p>
                    <p className="text-4xl font-bold text-orange-600">{results.overallScore}/100</p>
                  </div>
                  <div className="text-right">
                    <p className="text-gray-600">Cognitive Risk</p>
                    <p className="text-xl font-semibold text-green-600">Low</p>
                  </div>
                </div>
              </div>

              {/* Metrics */}
              <div className="grid md:grid-cols-2 gap-4 mb-8">
                {Object.entries(results.metrics).map(([key, value]: [string, any]) => (
                  <div key={key} className="bg-gray-50 rounded-xl p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold capitalize">{key.replace(/([A-Z])/g, ' $1')}</span>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                        value.status === 'Normal' ? 'bg-green-100 text-green-700' :
                        'bg-yellow-100 text-yellow-700'
                      }`}>
                        {value.status}
                      </span>
                    </div>
                    <div className="flex items-center mb-2">
                      <div className="flex-1 h-2 bg-gray-200 rounded-full mr-3">
                        <div
                          className="h-full bg-orange-500 rounded-full"
                          style={{ width: `${value.score}%` }}
                        />
                      </div>
                      <span className="font-bold text-orange-600">{value.score}%</span>
                    </div>
                    <p className="text-sm text-gray-600">{value.details}</p>
                  </div>
                ))}
              </div>

              {/* Cognitive Indicators */}
              <div className="bg-blue-50 rounded-xl p-6 mb-8">
                <h3 className="font-semibold mb-4">Cognitive Indicators</h3>
                <div className="grid grid-cols-4 gap-4">
                  {Object.entries(results.cognitiveIndicators).map(([key, value]: [string, any]) => (
                    <div key={key} className="text-center">
                      <p className="text-sm text-gray-600 capitalize mb-1">{key}</p>
                      <p className={`font-semibold ${
                        value === 'Normal' ? 'text-green-600' : 'text-yellow-600'
                      }`}>
                        {value}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Observations */}
              <div className="mb-8">
                <h3 className="font-semibold mb-3">Key Findings</h3>
                <ul className="space-y-2">
                  {results.observations.map((obs: string, i: number) => (
                    <li key={i} className="flex items-start">
                      <span className="text-orange-500 mr-2">•</span>
                      <span className="text-gray-700">{obs}</span>
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
                  className="px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition"
                >
                  View Full Report
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

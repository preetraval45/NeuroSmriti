'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function DemoPage() {
  const [currentStep, setCurrentStep] = useState(0)
  const [demoStarted, setDemoStarted] = useState(false)

  const demoSteps = [
    {
      title: 'Welcome to NeuroSmriti',
      description: 'An AI-powered platform for early Alzheimer\'s detection and personalized memory care.',
      image: 'brain',
      features: [
        'AI-powered early detection',
        'Personalized memory care plans',
        'Real-time cognitive tracking',
        'Family caregiver support'
      ]
    },
    {
      title: 'AI Brain Scan Analysis',
      description: 'Upload MRI scans for instant AI analysis that can detect early signs of Alzheimer\'s with 94% accuracy.',
      image: 'scan',
      demo: 'brain-scan'
    },
    {
      title: 'Cognitive Assessment Tests',
      description: 'Complete scientifically validated tests to measure memory, attention, language, and executive function.',
      image: 'test',
      demo: 'cognitive-test'
    },
    {
      title: 'Memory Care Dashboard',
      description: 'Track cognitive health, medications, daily activities, and care plans in one unified dashboard.',
      image: 'dashboard',
      demo: 'dashboard'
    },
    {
      title: 'Personalized Memory Exercises',
      description: 'AI-recommended games and activities to strengthen cognitive function and slow memory decline.',
      image: 'exercises',
      demo: 'memory-games'
    }
  ]

  const [brainScanDemo, setBrainScanDemo] = useState({
    uploaded: false,
    analyzing: false,
    complete: false,
    result: null as null | {
      stage: number
      confidence: number
      findings: string[]
    }
  })

  const simulateBrainScan = () => {
    setBrainScanDemo({ ...brainScanDemo, uploaded: true, analyzing: true })

    setTimeout(() => {
      setBrainScanDemo({
        uploaded: true,
        analyzing: false,
        complete: true,
        result: {
          stage: 2,
          confidence: 94,
          findings: [
            'Mild hippocampal atrophy detected',
            'Normal ventricular volume',
            'No significant white matter lesions',
            'Early memory region changes observed'
          ]
        }
      })
    }, 3000)
  }

  if (!demoStarted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full text-center">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-12">
            <div className="w-24 h-24 bg-gradient-to-br from-purple-400 to-blue-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h1 className="text-4xl font-bold text-white mb-4">Interactive Demo</h1>
            <p className="text-xl text-purple-200 mb-8">
              Experience how NeuroSmriti helps detect Alzheimer&apos;s early and provides personalized memory care.
            </p>
            <button
              onClick={() => setDemoStarted(true)}
              className="px-8 py-4 bg-white text-purple-600 rounded-xl font-bold text-lg hover:bg-purple-50 transition transform hover:scale-105"
            >
              Start Interactive Demo
            </button>
            <p className="mt-6 text-purple-300 text-sm">
              No signup required. Takes about 5 minutes.
            </p>
          </div>
        </div>
      </div>
    )
  }

  const currentStepData = demoSteps[currentStep]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Progress Bar */}
      <div className="fixed top-20 left-0 right-0 z-40 bg-white shadow">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Demo Progress</span>
            <span className="text-sm font-semibold text-purple-600">
              Step {currentStep + 1} of {demoSteps.length}
            </span>
          </div>
          <div className="mt-2 h-2 bg-gray-200 rounded-full">
            <div
              className="h-full bg-gradient-to-r from-purple-600 to-blue-500 rounded-full transition-all duration-500"
              style={{ width: `${((currentStep + 1) / demoSteps.length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 pt-32 pb-24">
        <div className="max-w-4xl mx-auto">
          {/* Step Content */}
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-8 text-white">
              <h2 className="text-3xl font-bold mb-2">{currentStepData.title}</h2>
              <p className="text-purple-100 text-lg">{currentStepData.description}</p>
            </div>

            {/* Demo Content */}
            <div className="p-8">
              {currentStep === 0 && (
                <div className="grid md:grid-cols-2 gap-6">
                  {currentStepData.features?.map((feature, i) => (
                    <div key={i} className="flex items-center bg-purple-50 rounded-xl p-4">
                      <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center mr-4">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <span className="font-medium text-gray-800">{feature}</span>
                    </div>
                  ))}
                </div>
              )}

              {currentStep === 1 && (
                <div className="text-center">
                  {!brainScanDemo.uploaded && (
                    <div
                      onClick={simulateBrainScan}
                      className="border-4 border-dashed border-purple-300 rounded-2xl p-12 cursor-pointer hover:bg-purple-50 transition"
                    >
                      <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg className="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                      </div>
                      <p className="text-lg font-semibold text-gray-800">Click to simulate MRI upload</p>
                      <p className="text-gray-500 mt-2">Demo will use sample brain scan data</p>
                    </div>
                  )}

                  {brainScanDemo.analyzing && (
                    <div className="py-12">
                      <div className="w-24 h-24 mx-auto mb-6 relative">
                        <div className="absolute inset-0 border-4 border-purple-200 rounded-full" />
                        <div className="absolute inset-0 border-4 border-purple-600 rounded-full border-t-transparent animate-spin" />
                        <div className="absolute inset-4 bg-purple-100 rounded-full flex items-center justify-center">
                          <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                          </svg>
                        </div>
                      </div>
                      <p className="text-lg font-semibold text-gray-800">AI Analyzing Brain Scan...</p>
                      <p className="text-gray-500">Processing neuroimaging data</p>
                    </div>
                  )}

                  {brainScanDemo.complete && brainScanDemo.result && (
                    <div className="space-y-6">
                      <div className="bg-green-50 border border-green-200 rounded-xl p-6">
                        <div className="flex items-center justify-center mb-4">
                          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                          </div>
                        </div>
                        <h3 className="text-xl font-bold text-green-800">Analysis Complete</h3>
                        <p className="text-green-600">Confidence: {brainScanDemo.result.confidence}%</p>
                      </div>

                      <div className="bg-purple-50 rounded-xl p-6">
                        <h4 className="font-bold text-gray-800 mb-4">Detection Results:</h4>
                        <div className="text-left">
                          <div className="flex items-center mb-3">
                            <span className="text-gray-600">Predicted Stage:</span>
                            <span className="ml-auto font-bold text-purple-600">Stage {brainScanDemo.result.stage} - Mild Cognitive Impairment</span>
                          </div>
                          <div className="space-y-2">
                            {brainScanDemo.result.findings.map((finding, i) => (
                              <div key={i} className="flex items-start">
                                <svg className="w-5 h-5 text-purple-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <span className="text-gray-700">{finding}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {currentStep === 2 && (
                <div className="space-y-6">
                  <p className="text-gray-600 mb-6">Our cognitive assessments test multiple domains:</p>
                  <div className="grid md:grid-cols-2 gap-4">
                    {[
                      { name: 'Memory Test', desc: 'Pattern recognition and recall', score: 85 },
                      { name: 'Attention Test', desc: 'Focus and concentration', score: 78 },
                      { name: 'Language Test', desc: 'Word finding and comprehension', score: 92 },
                      { name: 'Executive Function', desc: 'Planning and problem solving', score: 88 }
                    ].map((test, i) => (
                      <div key={i} className="bg-gray-50 rounded-xl p-4">
                        <div className="flex justify-between items-center mb-2">
                          <h4 className="font-semibold text-gray-800">{test.name}</h4>
                          <span className="text-purple-600 font-bold">{test.score}%</span>
                        </div>
                        <p className="text-sm text-gray-500 mb-2">{test.desc}</p>
                        <div className="h-2 bg-gray-200 rounded-full">
                          <div
                            className="h-full bg-purple-500 rounded-full transition-all duration-1000"
                            style={{ width: `${test.score}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                  <Link
                    href="/cognitive-tests"
                    className="inline-block px-6 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition"
                  >
                    Try Cognitive Tests
                  </Link>
                </div>
              )}

              {currentStep === 3 && (
                <div className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-4">
                    {[
                      { label: 'Cognitive Score', value: '85/100', trend: '+3' },
                      { label: 'Memory Score', value: '78/100', trend: '+5' },
                      { label: 'Daily Activities', value: '12/15', trend: '0' }
                    ].map((stat, i) => (
                      <div key={i} className="bg-purple-50 rounded-xl p-4 text-center">
                        <p className="text-sm text-gray-500">{stat.label}</p>
                        <p className="text-2xl font-bold text-purple-600">{stat.value}</p>
                        <p className={`text-sm ${parseInt(stat.trend) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {parseInt(stat.trend) >= 0 ? '+' : ''}{stat.trend} this week
                        </p>
                      </div>
                    ))}
                  </div>
                  <Link
                    href="/dashboard"
                    className="inline-block px-6 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition"
                  >
                    View Full Dashboard
                  </Link>
                </div>
              )}

              {currentStep === 4 && (
                <div className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-4">
                    {[
                      { name: 'Memory Match', desc: 'Classic card matching game', difficulty: 'Easy' },
                      { name: 'Word Recall', desc: 'Remember and type words', difficulty: 'Medium' },
                      { name: 'Pattern Sequence', desc: 'Follow the pattern', difficulty: 'Medium' },
                      { name: 'Daily Puzzles', desc: 'Brain training exercises', difficulty: 'Varies' }
                    ].map((game, i) => (
                      <div key={i} className="bg-gray-50 rounded-xl p-4 flex items-center">
                        <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mr-4">
                          <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-800">{game.name}</h4>
                          <p className="text-sm text-gray-500">{game.desc}</p>
                          <span className="text-xs text-purple-600">{game.difficulty}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                  <Link
                    href="/memory-games"
                    className="inline-block px-6 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition"
                  >
                    Play Memory Games
                  </Link>
                </div>
              )}
            </div>

            {/* Navigation */}
            <div className="p-6 bg-gray-50 flex justify-between">
              <button
                onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                disabled={currentStep === 0}
                className="px-6 py-3 border border-gray-300 rounded-xl font-semibold text-gray-600 hover:bg-gray-100 transition disabled:opacity-50"
              >
                Previous
              </button>
              {currentStep < demoSteps.length - 1 ? (
                <button
                  onClick={() => setCurrentStep(currentStep + 1)}
                  className="px-6 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition"
                >
                  Next Step
                </button>
              ) : (
                <Link
                  href="/register"
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-xl font-semibold hover:shadow-lg transition"
                >
                  Get Started Free
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

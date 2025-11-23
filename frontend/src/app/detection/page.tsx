'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function DetectionPage() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [activeTest, setActiveTest] = useState<string | null>(null)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFile(file)
      setResult(null)
    }
  }

  const analyzeImage = () => {
    setAnalyzing(true)
    // Simulate AI analysis
    setTimeout(() => {
      setResult({
        stage: 'Mild Cognitive Impairment',
        confidence: 94.2,
        riskScore: 0.42,
        findings: [
          { region: 'Hippocampus', status: 'Mild atrophy detected', severity: 'moderate' },
          { region: 'Temporal Lobe', status: 'Volume within normal range', severity: 'normal' },
          { region: 'Entorhinal Cortex', status: 'Early signs of thinning', severity: 'mild' },
          { region: 'Ventricular Space', status: 'Slight enlargement', severity: 'mild' }
        ],
        recommendations: [
          'Schedule follow-up MRI in 6 months',
          'Begin cognitive therapy program',
          'Consider cholinesterase inhibitor medication',
          'Enroll in memory preservation exercises'
        ]
      })
      setAnalyzing(false)
    }, 3000)
  }

  const cognitiveTests = [
    {
      id: 'memory',
      name: 'Memory Test',
      description: 'Assess short-term and long-term memory recall',
      duration: '10 min',
      icon: '🧠'
    },
    {
      id: 'attention',
      name: 'Attention & Focus',
      description: 'Measure concentration and attention span',
      duration: '8 min',
      icon: '🎯'
    },
    {
      id: 'language',
      name: 'Language Skills',
      description: 'Evaluate word-finding and verbal fluency',
      duration: '12 min',
      icon: '💬'
    },
    {
      id: 'spatial',
      name: 'Spatial Reasoning',
      description: 'Test visuospatial abilities and orientation',
      duration: '10 min',
      icon: '🔷'
    },
    {
      id: 'executive',
      name: 'Executive Function',
      description: 'Assess planning, problem-solving, and decision-making',
      duration: '15 min',
      icon: '📊'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-purple-700 to-indigo-800 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">AI-Powered Detection</h1>
            <p className="text-xl text-purple-100">
              Advanced multimodal analysis for early Alzheimer&apos;s detection with 94% accuracy
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          {/* Detection Methods */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Brain Scan Upload */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mr-4">
                  <span className="text-2xl">🧠</span>
                </div>
                <div>
                  <h2 className="text-2xl font-bold">Brain Scan Analysis</h2>
                  <p className="text-gray-600">Upload MRI or CT scan for AI analysis</p>
                </div>
              </div>

              <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-purple-500 transition cursor-pointer">
                <input
                  type="file"
                  accept="image/*,.nii,.dcm"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="scan-upload"
                />
                <label htmlFor="scan-upload" className="cursor-pointer">
                  {uploadedFile ? (
                    <div>
                      <span className="text-4xl mb-4 block">✅</span>
                      <p className="font-semibold text-green-600">{uploadedFile.name}</p>
                      <p className="text-sm text-gray-500 mt-2">Click to change file</p>
                    </div>
                  ) : (
                    <div>
                      <span className="text-4xl mb-4 block">📤</span>
                      <p className="font-semibold mb-2">Drop your scan here or click to upload</p>
                      <p className="text-sm text-gray-500">Supports MRI, CT, DICOM, NIfTI formats</p>
                    </div>
                  )}
                </label>
              </div>

              {uploadedFile && !result && (
                <button
                  onClick={analyzeImage}
                  disabled={analyzing}
                  className="w-full mt-6 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg transition disabled:opacity-50"
                >
                  {analyzing ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Analyzing with AI...
                    </span>
                  ) : (
                    'Analyze Brain Scan'
                  )}
                </button>
              )}

              {result && (
                <div className="mt-6 p-6 bg-gray-50 rounded-xl">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold">Analysis Results</h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      result.stage === 'Normal' ? 'bg-green-100 text-green-800' :
                      result.stage.includes('Mild') ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {result.confidence}% Confidence
                    </span>
                  </div>

                  <div className="mb-4">
                    <p className="text-gray-600">Detected Stage:</p>
                    <p className="text-2xl font-bold text-purple-600">{result.stage}</p>
                  </div>

                  <div className="mb-4">
                    <p className="text-gray-600 mb-2">Risk Score:</p>
                    <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 rounded-full"
                        style={{ width: `${result.riskScore * 100}%` }}
                      />
                    </div>
                    <p className="text-sm text-gray-500 mt-1">{(result.riskScore * 100).toFixed(1)}% risk level</p>
                  </div>

                  <div className="mb-4">
                    <p className="text-gray-600 mb-2">Brain Region Analysis:</p>
                    <div className="space-y-2">
                      {result.findings.map((finding: any, i: number) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-white rounded-lg">
                          <span className="font-medium">{finding.region}</span>
                          <span className={`text-sm ${
                            finding.severity === 'normal' ? 'text-green-600' :
                            finding.severity === 'mild' ? 'text-yellow-600' :
                            'text-orange-600'
                          }`}>
                            {finding.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <p className="text-gray-600 mb-2">Recommendations:</p>
                    <ul className="space-y-2">
                      {result.recommendations.map((rec: string, i: number) => (
                        <li key={i} className="flex items-start">
                          <span className="text-purple-600 mr-2">•</span>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="mt-6 flex gap-4">
                    <Link href="/treatment" className="flex-1 py-3 bg-purple-600 text-white rounded-xl text-center font-semibold hover:bg-purple-700 transition">
                      View Treatment Plans
                    </Link>
                    <button
                      type="button"
                      onClick={() => setResult(null)}
                      className="flex-1 py-3 border-2 border-purple-600 text-purple-600 rounded-xl font-semibold hover:bg-purple-50 transition"
                    >
                      New Analysis
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Cognitive Tests */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mr-4">
                  <span className="text-2xl">📝</span>
                </div>
                <div>
                  <h2 className="text-2xl font-bold">Cognitive Assessment</h2>
                  <p className="text-gray-600">Interactive tests to evaluate cognitive function</p>
                </div>
              </div>

              <div className="space-y-4">
                {cognitiveTests.map(test => (
                  <div
                    key={test.id}
                    className={`p-4 border-2 rounded-xl cursor-pointer transition ${
                      activeTest === test.id ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-purple-300'
                    }`}
                    onClick={() => setActiveTest(test.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className="text-2xl mr-3">{test.icon}</span>
                        <div>
                          <h3 className="font-semibold">{test.name}</h3>
                          <p className="text-sm text-gray-600">{test.description}</p>
                        </div>
                      </div>
                      <span className="text-sm text-gray-500">{test.duration}</span>
                    </div>
                  </div>
                ))}
              </div>

              <Link
                href="/cognitive-tests"
                className="block w-full mt-6 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-semibold hover:shadow-lg transition text-center"
              >
                Start {activeTest ? cognitiveTests.find(t => t.id === activeTest)?.name : 'Cognitive Assessment'}
              </Link>
            </div>
          </div>

          {/* Additional Detection Methods */}
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition">
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-4">
                <span className="text-2xl">🎤</span>
              </div>
              <h3 className="text-xl font-bold mb-2">Speech Analysis</h3>
              <p className="text-gray-600 mb-4">
                AI analyzes speech patterns, pauses, and word-finding difficulties for early detection markers.
              </p>
              <Link href="/speech-analysis" className="block w-full py-3 border-2 border-green-500 text-green-600 rounded-xl font-semibold hover:bg-green-50 transition text-center">
                Start Recording
              </Link>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition">
              <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4">
                <span className="text-2xl">👁️</span>
              </div>
              <h3 className="text-xl font-bold mb-2">Eye Tracking</h3>
              <p className="text-gray-600 mb-4">
                Monitor eye movements and reading patterns using your device camera to detect cognitive changes.
              </p>
              <Link href="/eye-tracking" className="block w-full py-3 border-2 border-orange-500 text-orange-600 rounded-xl font-semibold hover:bg-orange-50 transition text-center">
                Begin Eye Test
              </Link>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition">
              <div className="w-12 h-12 bg-pink-100 rounded-xl flex items-center justify-center mb-4">
                <span className="text-2xl">📱</span>
              </div>
              <h3 className="text-xl font-bold mb-2">Digital Biomarkers</h3>
              <p className="text-gray-600 mb-4">
                Analyze smartphone usage patterns, typing speed, and app interactions for continuous monitoring.
              </p>
              <Link href="/digital-biomarkers" className="block w-full py-3 border-2 border-pink-500 text-pink-600 rounded-xl font-semibold hover:bg-pink-50 transition text-center">
                Connect Device
              </Link>
            </div>
          </div>

          {/* Info Section */}
          <div className="mt-12 bg-gradient-to-r from-purple-100 to-blue-100 rounded-2xl p-8">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-2xl font-bold mb-4">Why Early Detection Matters</h2>
              <p className="text-gray-700 mb-6">
                Early detection of Alzheimer&apos;s disease can lead to better outcomes. When caught early,
                patients can benefit from treatments that slow progression, participate in clinical trials,
                and have more time to plan for the future with their loved ones.
              </p>
              <div className="grid grid-cols-3 gap-6 text-center">
                <div>
                  <div className="text-3xl font-bold text-purple-600">30%</div>
                  <div className="text-sm text-gray-600">Slower progression with early intervention</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-purple-600">6 Years</div>
                  <div className="text-sm text-gray-600">Earlier detection than traditional methods</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-purple-600">94%</div>
                  <div className="text-sm text-gray-600">Detection accuracy across all stages</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

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
    // Demo: Simulate AI analysis for research demonstration
    setTimeout(() => {
      setResult({
        stage: 'Research Demo - Simulated Analysis',
        confidence: 'N/A',
        riskScore: 0,
        findings: [
          { region: 'Hippocampus', status: 'Volume analysis - research feature', severity: 'normal' },
          { region: 'Temporal Lobe', status: 'Volumetric measurement - demo', severity: 'normal' },
          { region: 'Entorhinal Cortex', status: 'Thickness analysis - experimental', severity: 'normal' },
          { region: 'Ventricular Space', status: 'Size measurement - research tool', severity: 'normal' }
        ],
        recommendations: [
          'This is a research demonstration only',
          'Consult qualified healthcare professionals for medical advice',
          'Contact Alzheimer\'s Association at 1-800-272-3900 for clinical resources',
          'Do not use this platform for medical decision-making'
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
      <section className="bg-gradient-to-r from-indigo-700 via-purple-700 to-blue-700 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-block px-4 py-2 bg-amber-500 text-amber-900 rounded-full text-sm font-bold mb-4">
              RESEARCH PROTOTYPE - NOT FOR CLINICAL DIAGNOSIS
            </div>
            <h1 className="text-4xl md:text-6xl font-bold mb-6">Multimodal AI Detection Platform</h1>
            <p className="text-xl text-indigo-100 mb-4">
              Research tools for exploring early cognitive decline indicators through multiple data modalities
            </p>
            <p className="text-sm text-indigo-200 max-w-2xl mx-auto">
              This platform demonstrates experimental AI techniques for analyzing brain imaging, cognitive performance,
              speech patterns, and behavioral data. All results are for research purposes only.
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          {/* Detection Methods */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Brain Scan Upload */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border-l-4 border-indigo-500">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mr-4">
                    <span className="text-2xl">🧠</span>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">Neuroimaging Analysis</h2>
                    <p className="text-gray-600 text-sm">Research tool for brain scan exploration</p>
                  </div>
                </div>
                <div className="px-3 py-1 bg-amber-100 text-amber-800 text-xs font-semibold rounded-full">
                  DEMO
                </div>
              </div>

              <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 mb-4">
                <div className="flex items-start space-x-3 text-sm text-gray-700">
                  <span className="text-amber-600">⚠️</span>
                  <div>
                    <p className="font-semibold text-gray-900 mb-1">Research Demonstration Only</p>
                    <p className="text-xs text-gray-600">
                      This feature simulates AI analysis for educational purposes. No real medical diagnosis is performed.
                      Always consult healthcare professionals for actual medical evaluation.
                    </p>
                  </div>
                </div>
              </div>

              <div className="border-2 border-dashed border-indigo-300 rounded-xl p-8 text-center hover:border-indigo-500 transition cursor-pointer bg-gray-50">
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
                      <p className="font-semibold text-indigo-600">{uploadedFile.name}</p>
                      <p className="text-sm text-gray-500 mt-2">Click to change file</p>
                    </div>
                  ) : (
                    <div>
                      <span className="text-4xl mb-4 block">📤</span>
                      <p className="font-semibold mb-2 text-gray-900">Drop scan file or click to upload</p>
                      <p className="text-sm text-gray-500">Supports: MRI, CT, DICOM (.dcm), NIfTI (.nii) formats</p>
                      <p className="text-xs text-gray-400 mt-2">Demo mode - analysis is simulated</p>
                    </div>
                  )}
                </label>
              </div>

              {uploadedFile && !result && (
                <button
                  type="button"
                  onClick={analyzeImage}
                  disabled={analyzing}
                  className="w-full mt-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {analyzing ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Running Demo Analysis...
                    </span>
                  ) : (
                    'Run Demo Analysis (Research Only)'
                  )}
                </button>
              )}

              {result && (
                <div className="mt-6 p-6 bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl border-2 border-amber-300">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-bold text-gray-900">Demo Results</h3>
                    <span className="px-4 py-2 rounded-full text-sm font-bold bg-amber-200 text-amber-900">
                      SIMULATED - NOT REAL
                    </span>
                  </div>

                  <div className="mb-6 p-4 bg-white rounded-lg border-l-4 border-red-500">
                    <p className="font-bold text-red-900 mb-2">⚠️ Critical Disclaimer</p>
                    <p className="text-sm text-red-800">
                      This is a simulated demo result. <strong>NO real medical analysis has been performed.</strong>
                      This platform cannot diagnose Alzheimer&apos;s disease or any medical condition.
                      Always seek professional medical evaluation from qualified healthcare providers.
                    </p>
                  </div>

                  <div className="mb-4">
                    <p className="text-gray-600 text-sm">Demo Status:</p>
                    <p className="text-xl font-bold text-indigo-600">{result.stage}</p>
                  </div>

                  <div className="mb-4">
                    <p className="text-gray-600 mb-2 text-sm">Simulated Feature Analysis:</p>
                    <div className="space-y-2">
                      {result.findings.map((finding: any, i: number) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200">
                          <span className="font-medium text-gray-900">{finding.region}</span>
                          <span className="text-xs text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
                            {finding.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mb-6">
                    <p className="text-gray-600 mb-2 text-sm font-semibold">Important Information:</p>
                    <ul className="space-y-2">
                      {result.recommendations.map((rec: string, i: number) => (
                        <li key={i} className="flex items-start p-2 bg-white rounded-lg">
                          <span className="text-indigo-600 mr-2 font-bold">•</span>
                          <span className="text-sm text-gray-700">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-sm text-blue-900 font-semibold mb-2">Need Real Medical Help?</p>
                    <p className="text-sm text-blue-800 mb-3">
                      Contact the Alzheimer&apos;s Association 24/7 Helpline for professional guidance and support.
                    </p>
                    <a
                      href="tel:+18002723900"
                      className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
                    >
                      Call 1-800-272-3900
                    </a>
                  </div>

                  <div className="mt-4 flex gap-4">
                    <button
                      type="button"
                      onClick={() => setResult(null)}
                      className="flex-1 py-3 border-2 border-indigo-600 text-indigo-600 rounded-xl font-semibold hover:bg-indigo-50 transition"
                    >
                      Run Another Demo
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Cognitive Tests */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border-l-4 border-blue-500">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mr-4">
                    <span className="text-2xl">📝</span>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">Cognitive Assessment Tools</h2>
                    <p className="text-gray-600 text-sm">Research-based cognitive evaluation</p>
                  </div>
                </div>
                <div className="px-3 py-1 bg-amber-100 text-amber-800 text-xs font-semibold rounded-full">
                  DEMO
                </div>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-6 mb-4">
                <div className="flex items-start space-x-3 text-sm text-gray-700">
                  <span className="text-amber-600">⚠️</span>
                  <div>
                    <p className="font-semibold text-gray-900 mb-1">Research Tools Only</p>
                    <p className="text-xs text-gray-600">
                      These cognitive tests are experimental research tools and cannot diagnose or assess medical conditions.
                      For clinical cognitive assessment, please consult a neurologist or neuropsychologist.
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                {cognitiveTests.map(test => (
                  <button
                    key={test.id}
                    type="button"
                    className={`w-full p-4 border-2 rounded-xl transition text-left ${
                      activeTest === test.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                    }`}
                    onClick={() => setActiveTest(test.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className="text-2xl mr-3">{test.icon}</span>
                        <div>
                          <h3 className="font-semibold text-gray-900">{test.name}</h3>
                          <p className="text-sm text-gray-600">{test.description}</p>
                        </div>
                      </div>
                      <span className="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full">{test.duration}</span>
                    </div>
                  </button>
                ))}
              </div>

              <Link
                href="/cognitive-tests"
                className="block w-full mt-6 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-semibold hover:shadow-lg transition text-center"
              >
                Explore {activeTest ? cognitiveTests.find(t => t.id === activeTest)?.name : 'Cognitive Tests'} (Demo)
              </Link>
            </div>
          </div>

          {/* Additional Detection Methods */}
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition border-t-4 border-green-500">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">🎤</span>
                </div>
                <span className="px-2 py-1 bg-amber-100 text-amber-800 text-xs font-bold rounded">EXPERIMENTAL</span>
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-900">Speech Pattern Analysis</h3>
              <p className="text-gray-600 text-sm mb-4">
                Research tool for exploring speech characteristics like pausing, word selection, and fluency patterns.
                Not for clinical diagnosis.
              </p>
              <Link href="/speech-analysis" className="block w-full py-3 border-2 border-green-500 text-green-600 rounded-xl font-semibold hover:bg-green-50 transition text-center">
                Explore Demo
              </Link>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition border-t-4 border-orange-500">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">👁️</span>
                </div>
                <span className="px-2 py-1 bg-amber-100 text-amber-800 text-xs font-bold rounded">EXPERIMENTAL</span>
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-900">Eye Movement Research</h3>
              <p className="text-gray-600 text-sm mb-4">
                Experimental tool for studying eye tracking patterns and reading behaviors using device camera.
                Research purposes only.
              </p>
              <Link href="/eye-tracking" className="block w-full py-3 border-2 border-orange-500 text-orange-600 rounded-xl font-semibold hover:bg-orange-50 transition text-center">
                Explore Demo
              </Link>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition border-t-4 border-pink-500">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-pink-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">📱</span>
                </div>
                <span className="px-2 py-1 bg-amber-100 text-amber-800 text-xs font-bold rounded">EXPERIMENTAL</span>
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-900">Digital Behavior Patterns</h3>
              <p className="text-gray-600 text-sm mb-4">
                Research tool for analyzing device interaction patterns like typing speed and app usage.
                Not for medical monitoring.
              </p>
              <Link href="/digital-biomarkers" className="block w-full py-3 border-2 border-pink-500 text-pink-600 rounded-xl font-semibold hover:bg-pink-50 transition text-center">
                Explore Demo
              </Link>
            </div>
          </div>

          {/* Info Section */}
          <div className="mt-12 bg-gradient-to-br from-indigo-50 via-purple-50 to-blue-50 rounded-2xl p-8 border-2 border-indigo-200">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl font-bold mb-4 text-gray-900">Research Goals & Clinical Relevance</h2>
              <p className="text-gray-700 mb-6 leading-relaxed">
                This research platform explores AI techniques for early cognitive decline detection.
                While these are experimental tools, they&apos;re based on established research showing that
                early detection enables access to emerging treatments, clinical trial participation, and
                advance care planning with healthcare providers and families.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                <div className="bg-white rounded-xl p-6 shadow-md">
                  <div className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Research Focus</div>
                  <div className="text-sm text-gray-600 mt-2">Multimodal AI analysis techniques</div>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-md">
                  <div className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Real Datasets</div>
                  <div className="text-sm text-gray-600 mt-2">ADNI, OASIS, NACC, DementiaBank</div>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-md">
                  <div className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Clinical Partners</div>
                  <div className="text-sm text-gray-600 mt-2">Collaborating with medical researchers</div>
                </div>
              </div>

              <div className="mt-8 p-6 bg-blue-100 rounded-xl border-2 border-blue-300">
                <p className="text-sm text-blue-900 font-semibold mb-2">For Clinical Evaluation & Support</p>
                <p className="text-sm text-blue-800 mb-3">
                  Contact the Alzheimer&apos;s Association for professional medical guidance, diagnostic resources, and caregiver support.
                </p>
                <a
                  href="tel:+18002723900"
                  className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
                >
                  24/7 Helpline: 1-800-272-3900
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

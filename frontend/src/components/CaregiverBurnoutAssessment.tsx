'use client'

import React, { useState, useEffect } from 'react'

interface AssessmentResult {
  burnout_score: number
  risk_level: string
  urgency: string
  stress_indicators: Record<string, number>
  recommendations: Array<{
    priority: string
    category: string
    title: string
    description: string
    resources: string[]
  }>
}

export default function CaregiverBurnoutAssessment({ caregiverId }: { caregiverId: number }) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [responses, setResponses] = useState<Record<string, number>>({})
  const [result, setResult] = useState<AssessmentResult | null>(null)
  const [showResources, setShowResources] = useState(false)
  const [stressTrend, setStressTrend] = useState<any>(null)

  const questions = [
    {
      key: 'feel_overwhelmed',
      question: 'How often do you feel overwhelmed by caregiving responsibilities?',
      description: '1 = Never, 5 = Constantly'
    },
    {
      key: 'time_for_self',
      question: 'How much time do you have for yourself and your own needs?',
      description: '1 = None, 5 = Plenty'
    },
    {
      key: 'emotional_strain',
      question: 'How emotionally drained do you feel?',
      description: '1 = Not at all, 5 = Extremely'
    },
    {
      key: 'physical_exhaustion',
      question: 'How physically exhausted are you?',
      description: '1 = Not at all, 5 = Completely exhausted'
    },
    {
      key: 'sleep_quality',
      question: 'How would you rate your sleep quality?',
      description: '1 = Very poor, 5 = Excellent'
    },
    {
      key: 'social_isolation',
      question: 'How isolated do you feel from friends and family?',
      description: '1 = Not isolated, 5 = Very isolated'
    },
    {
      key: 'financial_stress',
      question: 'How stressed are you about financial aspects of caregiving?',
      description: '1 = Not stressed, 5 = Extremely stressed'
    },
    {
      key: 'relationship_strain',
      question: 'How strained are your relationships due to caregiving?',
      description: '1 = Not strained, 5 = Very strained'
    }
  ]

  useEffect(() => {
    fetchStressTrend()
  }, [caregiverId])

  const fetchStressTrend = async () => {
    try {
      const response = await fetch(`/api/v1/safety/caregiver/stress-trend/${caregiverId}?days=30`)
      if (response.ok) {
        const data = await response.json()
        setStressTrend(data)
      }
    } catch (error) {
      console.error('Error fetching stress trend:', error)
    }
  }

  const handleResponse = (value: number) => {
    setResponses({ ...responses, [questions[currentQuestion].key]: value })

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      submitAssessment({ ...responses, [questions[currentQuestion].key]: value })
    }
  }

  const submitAssessment = async (allResponses: Record<string, number>) => {
    try {
      const response = await fetch('/api/v1/safety/caregiver/assess-burnout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          caregiver_id: caregiverId,
          responses: allResponses
        })
      })

      if (response.ok) {
        const data = await response.json()
        setResult(data)
      }
    } catch (error) {
      console.error('Error submitting assessment:', error)
      alert('Error submitting assessment')
    }
  }

  const resetAssessment = () => {
    setCurrentQuestion(0)
    setResponses({})
    setResult(null)
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'critical': return 'text-red-600 bg-red-50 border-red-200'
      case 'high': return 'text-orange-600 bg-orange-50 border-orange-200'
      case 'moderate': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      default: return 'text-green-600 bg-green-50 border-green-200'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-800'
      case 'high': return 'bg-orange-100 text-orange-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }

  if (result) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        {/* Results Header */}
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Assessment Results</h2>
          <div className={`inline-block px-6 py-3 rounded-lg border-2 ${getRiskColor(result.risk_level)}`}>
            <p className="text-sm font-semibold mb-1">Burnout Risk Level</p>
            <p className="text-3xl font-bold capitalize">{result.risk_level}</p>
            <p className="text-sm mt-1">Score: {result.burnout_score.toFixed(1)}/100</p>
          </div>
        </div>

        {/* Burnout Score Gauge */}
        <div className="mb-6">
          <div className="relative pt-1">
            <div className="flex mb-2 items-center justify-between">
              <div>
                <span className="text-xs font-semibold inline-block text-gray-700">
                  Burnout Score
                </span>
              </div>
              <div className="text-right">
                <span className="text-xs font-semibold inline-block text-gray-700">
                  {result.burnout_score.toFixed(1)}%
                </span>
              </div>
            </div>
            <div className="overflow-hidden h-4 mb-4 text-xs flex rounded-full bg-gray-200">
              <div
                style={{ width: `${result.burnout_score}%` }}
                className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center transition-all duration-500 ${
                  result.burnout_score >= 70 ? 'bg-red-500' :
                  result.burnout_score >= 50 ? 'bg-orange-500' :
                  result.burnout_score >= 30 ? 'bg-yellow-500' :
                  'bg-green-500'
                }`}
              ></div>
            </div>
          </div>
        </div>

        {/* Stress Indicators */}
        <div className="mb-6">
          <h3 className="font-semibold text-gray-700 mb-3">Stress Indicators</h3>
          <div className="grid grid-cols-2 gap-3">
            {Object.entries(result.stress_indicators).map(([key, value]) => (
              <div key={key} className="p-3 bg-gray-50 rounded-lg">
                <p className="text-xs text-gray-600 capitalize mb-1">
                  {key.replace(/_/g, ' ')}
                </p>
                <div className="flex items-center">
                  <div className="flex-1 h-2 bg-gray-200 rounded-full mr-2">
                    <div
                      className={`h-2 rounded-full ${
                        value >= 4 ? 'bg-red-500' :
                        value >= 3 ? 'bg-orange-500' :
                        value >= 2 ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`}
                      style={{ width: `${(value / 5) * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-700">{value}/5</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="mb-6">
          <h3 className="font-semibold text-gray-700 mb-3">Recommendations</h3>
          <div className="space-y-3">
            {result.recommendations.map((rec, idx) => (
              <div key={idx} className="p-4 border border-gray-200 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <span className={`text-xs font-semibold px-2 py-1 rounded ${getPriorityColor(rec.priority)}`}>
                      {rec.priority.toUpperCase()}
                    </span>
                    <h4 className="font-semibold text-gray-900 mt-2">{rec.title}</h4>
                  </div>
                </div>
                <p className="text-sm text-gray-700 mb-2">{rec.description}</p>
                {rec.resources.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs font-semibold text-gray-600 mb-1">Resources:</p>
                    <ul className="list-disc list-inside space-y-1">
                      {rec.resources.map((resource, ridx) => (
                        <li key={ridx} className="text-xs text-gray-600">{resource}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Stress Trend */}
        {stressTrend && stressTrend.status !== 'no_data' && (
          <div className="mb-6 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold text-gray-700 mb-2">30-Day Trend</h3>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-blue-600">{stressTrend.assessments_count}</p>
                <p className="text-xs text-gray-600">Assessments</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-blue-600">{stressTrend.average_score?.toFixed(1)}</p>
                <p className="text-xs text-gray-600">Average Score</p>
              </div>
              <div>
                <p className={`text-2xl font-bold capitalize ${
                  stressTrend.trend === 'increasing' ? 'text-red-600' :
                  stressTrend.trend === 'decreasing' ? 'text-green-600' :
                  'text-gray-600'
                }`}>
                  {stressTrend.trend === 'increasing' ? '↑' : stressTrend.trend === 'decreasing' ? '↓' : '→'}
                </p>
                <p className="text-xs text-gray-600 capitalize">{stressTrend.trend}</p>
              </div>
            </div>
          </div>
        )}

        {/* Support Resources Button */}
        <button
          onClick={() => setShowResources(!showResources)}
          className="w-full mb-4 px-4 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold transition"
        >
          {showResources ? 'Hide' : 'Show'} Support Resources
        </button>

        {showResources && (
          <div className="mb-6 p-4 bg-purple-50 border border-purple-200 rounded-lg">
            <h3 className="font-semibold text-gray-700 mb-3">Caregiver Support Resources</h3>
            <div className="space-y-3">
              <div>
                <p className="font-semibold text-sm text-gray-700 mb-1">24/7 Hotlines</p>
                <ul className="space-y-1 text-sm">
                  <li>📞 Alzheimer's Association: <span className="font-mono">1-800-272-3900</span></li>
                  <li>📞 Caregiver Action Network: <span className="font-mono">1-855-227-3640</span></li>
                </ul>
              </div>
              <div>
                <p className="font-semibold text-sm text-gray-700 mb-1">Online Communities</p>
                <ul className="space-y-1 text-sm text-blue-600">
                  <li>• Alzheimer's Association Online Community</li>
                  <li>• Caregiver Support Group Forums</li>
                  <li>• Family Caregiver Alliance</li>
                </ul>
              </div>
              <div>
                <p className="font-semibold text-sm text-gray-700 mb-1">Local Services</p>
                <ul className="space-y-1 text-sm">
                  <li>• Adult Day Care Programs</li>
                  <li>• Respite Care Services</li>
                  <li>• Caregiver Counseling</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex space-x-3">
          <button
            onClick={resetAssessment}
            className="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition"
          >
            Take Again
          </button>
          <button
            onClick={() => window.print()}
            className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
          >
            Print Results
          </button>
        </div>
      </div>
    )
  }

  // Assessment Questions UI
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Caregiver Burnout Assessment</h2>
        <p className="text-gray-600">
          Answer these questions honestly to assess your stress levels
        </p>
      </div>

      {/* Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600">
            Question {currentQuestion + 1} of {questions.length}
          </span>
          <span className="text-sm font-semibold text-blue-600">
            {Math.round(((currentQuestion + 1) / questions.length) * 100)}%
          </span>
        </div>
        <div className="w-full h-2 bg-gray-200 rounded-full">
          <div
            className="h-2 bg-blue-600 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Current Question */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {questions[currentQuestion].question}
        </h3>
        <p className="text-sm text-gray-600 mb-6">
          {questions[currentQuestion].description}
        </p>

        {/* Rating Scale */}
        <div className="grid grid-cols-5 gap-3">
          {[1, 2, 3, 4, 5].map((value) => (
            <button
              key={value}
              onClick={() => handleResponse(value)}
              className="p-4 border-2 border-gray-300 hover:border-blue-500 hover:bg-blue-50 rounded-lg transition text-center group"
            >
              <div className="text-3xl font-bold text-gray-700 group-hover:text-blue-600 mb-1">
                {value}
              </div>
              <div className="text-xs text-gray-500">
                {value === 1 ? 'Very Low' : value === 5 ? 'Very High' : ''}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Navigation */}
      {currentQuestion > 0 && (
        <button
          onClick={() => setCurrentQuestion(currentQuestion - 1)}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition"
        >
          ← Previous
        </button>
      )}

      {/* Info */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          💡 This assessment is based on validated caregiver stress scales. Your responses are confidential and will help us provide personalized support recommendations.
        </p>
      </div>
    </div>
  )
}

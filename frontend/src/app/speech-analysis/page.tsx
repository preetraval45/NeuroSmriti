'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'

export default function SpeechAnalysisPage() {
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [currentTask, setCurrentTask] = useState(0)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const timerRef = useRef<NodeJS.Timeout | null>(null)

  const speechTasks = [
    {
      id: 1,
      title: 'Picture Description',
      instruction: 'Describe what you see in the image below in as much detail as possible.',
      image: '🏠🌳👨‍👩‍👧‍👦🐕',
      duration: 60
    },
    {
      id: 2,
      title: 'Word Recall',
      instruction: 'Name as many animals as you can think of in 60 seconds.',
      duration: 60
    },
    {
      id: 3,
      title: 'Story Retelling',
      instruction: 'Listen to the short story, then retell it in your own words.',
      story: 'Maria went to the grocery store on Tuesday. She bought apples, bread, and milk. On her way home, she met her neighbor John, who was walking his dog. They talked about the weather and upcoming community picnic.',
      duration: 90
    },
    {
      id: 4,
      title: 'Sentence Completion',
      instruction: 'Complete each sentence with appropriate words.',
      sentences: [
        'The sun rises in the...',
        'When it rains, I use an...',
        'Birds fly in the...'
      ],
      duration: 45
    }
  ]

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
        }
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        setAudioBlob(blob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setRecordingTime(0)

      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
    } catch (err) {
      alert('Please allow microphone access to use speech analysis.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }

  const analyzeRecording = () => {
    setAnalyzing(true)
    // Simulate AI analysis
    setTimeout(() => {
      setResults({
        overallScore: 78,
        metrics: {
          speechRate: { score: 82, description: 'Words per minute within normal range' },
          pausePatterns: { score: 71, description: 'Slightly increased pause frequency detected' },
          wordFinding: { score: 75, description: 'Minor word-finding hesitations observed' },
          fluency: { score: 85, description: 'Good overall speech fluency' },
          coherence: { score: 77, description: 'Logical thought progression maintained' }
        },
        observations: [
          'Speech rate is consistent with age-matched norms',
          'Some hesitation patterns noted during complex descriptions',
          'Vocabulary usage is varied and appropriate',
          'Minor pauses during word retrieval tasks'
        ],
        recommendations: [
          'Consider regular cognitive exercises',
          'Practice word association games',
          'Schedule follow-up assessment in 3 months'
        ],
        riskLevel: 'low'
      })
      setAnalyzing(false)
    }, 3000)
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const nextTask = () => {
    if (currentTask < speechTasks.length - 1) {
      setCurrentTask(prev => prev + 1)
      setAudioBlob(null)
      setResults(null)
    }
  }

  const task = speechTasks[currentTask]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-green-600 to-teal-600 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Link href="/detection" className="inline-flex items-center text-green-100 hover:text-white mb-4">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Detection
            </Link>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Speech Analysis</h1>
            <p className="text-xl text-green-100">
              AI-powered analysis of speech patterns for early cognitive assessment
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Progress */}
          <div className="mb-8">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Task {currentTask + 1} of {speechTasks.length}</span>
              <span>{Math.round(((currentTask + 1) / speechTasks.length) * 100)}% Complete</span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full">
              <div
                className="h-full bg-green-500 rounded-full transition-all"
                style={{ width: `${((currentTask + 1) / speechTasks.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Task Card */}
          <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mr-4">
                <span className="text-2xl">🎤</span>
              </div>
              <div>
                <h2 className="text-2xl font-bold">{task.title}</h2>
                <p className="text-gray-600">Duration: {task.duration} seconds</p>
              </div>
            </div>

            <div className="bg-gray-50 rounded-xl p-6 mb-6">
              <p className="text-lg text-gray-700 mb-4">{task.instruction}</p>
              {task.image && (
                <div className="text-6xl text-center py-8 bg-white rounded-lg">
                  {task.image}
                </div>
              )}
              {task.story && (
                <div className="bg-white rounded-lg p-4 border-l-4 border-green-500">
                  <p className="text-gray-700 italic">&quot;{task.story}&quot;</p>
                </div>
              )}
              {task.sentences && (
                <ul className="space-y-2 bg-white rounded-lg p-4">
                  {task.sentences.map((sentence, i) => (
                    <li key={i} className="text-gray-700">• {sentence}</li>
                  ))}
                </ul>
              )}
            </div>

            {/* Recording Controls */}
            <div className="text-center">
              {!audioBlob && !results && (
                <div>
                  {isRecording ? (
                    <div className="space-y-4">
                      <div className="flex items-center justify-center space-x-3">
                        <div className="w-4 h-4 bg-red-500 rounded-full animate-pulse" />
                        <span className="text-2xl font-mono font-bold">{formatTime(recordingTime)}</span>
                      </div>
                      <button
                        type="button"
                        onClick={stopRecording}
                        className="px-8 py-4 bg-red-500 text-white rounded-xl font-semibold hover:bg-red-600 transition"
                      >
                        Stop Recording
                      </button>
                    </div>
                  ) : (
                    <button
                      type="button"
                      onClick={startRecording}
                      className="px-8 py-4 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition flex items-center mx-auto"
                    >
                      <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                      </svg>
                      Start Recording
                    </button>
                  )}
                </div>
              )}

              {audioBlob && !results && (
                <div className="space-y-4">
                  <div className="flex items-center justify-center space-x-2 text-green-600">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="font-semibold">Recording complete! Duration: {formatTime(recordingTime)}</span>
                  </div>
                  <div className="flex justify-center space-x-4">
                    <button
                      type="button"
                      onClick={() => setAudioBlob(null)}
                      className="px-6 py-3 border-2 border-gray-300 text-gray-600 rounded-xl font-semibold hover:bg-gray-50 transition"
                    >
                      Record Again
                    </button>
                    <button
                      type="button"
                      onClick={analyzeRecording}
                      disabled={analyzing}
                      className="px-6 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition disabled:opacity-50"
                    >
                      {analyzing ? 'Analyzing...' : 'Analyze Speech'}
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Results */}
            {results && (
              <div className="mt-8 border-t pt-8">
                <h3 className="text-xl font-bold mb-6">Analysis Results</h3>

                {/* Overall Score */}
                <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-xl p-6 mb-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-gray-600">Overall Cognitive Score</p>
                      <p className="text-4xl font-bold text-green-600">{results.overallScore}/100</p>
                    </div>
                    <div className={`px-4 py-2 rounded-full font-semibold ${
                      results.riskLevel === 'low' ? 'bg-green-100 text-green-700' :
                      results.riskLevel === 'moderate' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {results.riskLevel.charAt(0).toUpperCase() + results.riskLevel.slice(1)} Risk
                    </div>
                  </div>
                </div>

                {/* Metrics */}
                <div className="grid md:grid-cols-2 gap-4 mb-6">
                  {Object.entries(results.metrics).map(([key, value]: [string, any]) => (
                    <div key={key} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium capitalize">{key.replace(/([A-Z])/g, ' $1')}</span>
                        <span className={`font-bold ${
                          value.score >= 80 ? 'text-green-600' :
                          value.score >= 60 ? 'text-yellow-600' :
                          'text-red-600'
                        }`}>{value.score}%</span>
                      </div>
                      <p className="text-sm text-gray-600">{value.description}</p>
                    </div>
                  ))}
                </div>

                {/* Observations */}
                <div className="mb-6">
                  <h4 className="font-semibold mb-3">Key Observations</h4>
                  <ul className="space-y-2">
                    {results.observations.map((obs: string, i: number) => (
                      <li key={i} className="flex items-start">
                        <span className="text-green-500 mr-2">•</span>
                        <span className="text-gray-700">{obs}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Recommendations */}
                <div className="bg-blue-50 rounded-xl p-6">
                  <h4 className="font-semibold mb-3">Recommendations</h4>
                  <ul className="space-y-2">
                    {results.recommendations.map((rec: string, i: number) => (
                      <li key={i} className="flex items-start">
                        <span className="text-blue-500 mr-2">→</span>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Next Task Button */}
                <div className="mt-6 flex justify-between">
                  <Link
                    href="/detection"
                    className="px-6 py-3 border-2 border-gray-300 text-gray-600 rounded-xl font-semibold hover:bg-gray-50 transition"
                  >
                    Back to Detection
                  </Link>
                  {currentTask < speechTasks.length - 1 ? (
                    <button
                      type="button"
                      onClick={nextTask}
                      className="px-6 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition"
                    >
                      Next Task
                    </button>
                  ) : (
                    <Link
                      href="/dashboard"
                      className="px-6 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition"
                    >
                      View Full Report
                    </Link>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Info */}
          <div className="bg-gradient-to-r from-green-100 to-teal-100 rounded-2xl p-6">
            <h3 className="font-bold mb-3">About Speech Analysis</h3>
            <p className="text-gray-700">
              Our AI analyzes multiple aspects of your speech including articulation, word choice,
              sentence structure, and response patterns. Research shows that subtle changes in speech
              can be early indicators of cognitive changes, often appearing years before other symptoms.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

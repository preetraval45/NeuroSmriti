'use client'

import { useState, useEffect, useCallback } from 'react'
import Link from 'next/link'

type TestType = 'memory' | 'attention' | 'language' | 'spatial' | 'executive' | null

interface TestResult {
  testType: string
  score: number
  maxScore: number
  timeSpent: number
  details: string[]
}

export default function CognitiveTestsPage() {
  const [selectedTest, setSelectedTest] = useState<TestType>(null)
  const [testPhase, setTestPhase] = useState<'intro' | 'running' | 'complete'>('intro')
  const [results, setResults] = useState<TestResult[]>([])

  const tests = [
    {
      id: 'memory' as TestType,
      name: 'Memory Test',
      description: 'Test your ability to remember sequences and patterns',
      duration: '3 min',
      icon: '🧠'
    },
    {
      id: 'attention' as TestType,
      name: 'Attention Test',
      description: 'Measure your focus and concentration abilities',
      duration: '2 min',
      icon: '🎯'
    },
    {
      id: 'language' as TestType,
      name: 'Language Test',
      description: 'Assess word finding and verbal fluency',
      duration: '3 min',
      icon: '💬'
    },
    {
      id: 'spatial' as TestType,
      name: 'Spatial Reasoning',
      description: 'Test visual-spatial processing abilities',
      duration: '3 min',
      icon: '🔷'
    },
    {
      id: 'executive' as TestType,
      name: 'Executive Function',
      description: 'Evaluate planning and problem-solving skills',
      duration: '4 min',
      icon: '⚡'
    }
  ]

  const handleTestComplete = (result: TestResult) => {
    setResults([...results, result])
    setTestPhase('complete')
  }

  if (selectedTest && testPhase === 'running') {
    return (
      <TestRunner
        testType={selectedTest}
        onComplete={handleTestComplete}
        onExit={() => {
          setSelectedTest(null)
          setTestPhase('intro')
        }}
      />
    )
  }

  if (testPhase === 'complete') {
    const latestResult = results[results.length - 1]
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Test Complete!</h2>
              <p className="text-gray-600 mb-6">{latestResult.testType}</p>

              <div className="bg-purple-50 rounded-xl p-6 mb-6">
                <div className="text-5xl font-bold text-purple-600 mb-2">
                  {Math.round((latestResult.score / latestResult.maxScore) * 100)}%
                </div>
                <p className="text-gray-600">
                  Score: {latestResult.score} / {latestResult.maxScore}
                </p>
                <p className="text-sm text-gray-500">
                  Time: {Math.round(latestResult.timeSpent / 1000)}s
                </p>
              </div>

              <div className="text-left mb-6">
                <h4 className="font-semibold text-gray-800 mb-3">Performance Summary:</h4>
                <ul className="space-y-2">
                  {latestResult.details.map((detail, i) => (
                    <li key={i} className="flex items-start">
                      <svg className="w-5 h-5 text-purple-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span className="text-gray-700">{detail}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={() => {
                    setSelectedTest(null)
                    setTestPhase('intro')
                  }}
                  className="flex-1 py-3 border border-purple-600 text-purple-600 rounded-xl font-semibold hover:bg-purple-50 transition"
                >
                  More Tests
                </button>
                <Link
                  href="/dashboard"
                  className="flex-1 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition text-center"
                >
                  View Dashboard
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-purple-600 to-blue-600 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Cognitive Assessment Tests</h1>
            <p className="text-xl text-purple-100">
              Scientifically validated tests to measure your cognitive health
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Test Selection */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {tests.map((test) => (
              <button
                key={test.id}
                onClick={() => {
                  setSelectedTest(test.id)
                  setTestPhase('running')
                }}
                className="bg-white rounded-2xl shadow-lg p-6 text-left hover:shadow-xl transition transform hover:-translate-y-1"
              >
                <span className="text-4xl mb-4 block">{test.icon}</span>
                <h3 className="text-xl font-bold text-gray-800 mb-2">{test.name}</h3>
                <p className="text-gray-600 text-sm mb-4">{test.description}</p>
                <div className="flex items-center text-purple-600">
                  <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-sm font-semibold">{test.duration}</span>
                </div>
              </button>
            ))}
          </div>

          {/* Previous Results */}
          {results.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold mb-4">Your Test History</h3>
              <div className="space-y-4">
                {results.map((result, i) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div>
                      <h4 className="font-semibold text-gray-800">{result.testType}</h4>
                      <p className="text-sm text-gray-500">
                        Completed just now
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-purple-600">
                        {Math.round((result.score / result.maxScore) * 100)}%
                      </div>
                      <div className="text-sm text-gray-500">
                        {result.score}/{result.maxScore}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// Test Runner Component
function TestRunner({
  testType,
  onComplete,
  onExit
}: {
  testType: TestType
  onComplete: (result: TestResult) => void
  onExit: () => void
}) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [score, setScore] = useState(0)
  const [startTime] = useState(Date.now())
  const [showSequence, setShowSequence] = useState(true)
  const [userInput, setUserInput] = useState<number[]>([])
  const [sequence, setSequence] = useState<number[]>([])
  const [feedback, setFeedback] = useState<'correct' | 'wrong' | null>(null)

  // Memory Test: Remember the sequence
  const generateSequence = useCallback((length: number) => {
    const newSeq = Array.from({ length }, () => Math.floor(Math.random() * 9) + 1)
    setSequence(newSeq)
    setShowSequence(true)
    setUserInput([])

    setTimeout(() => {
      setShowSequence(false)
    }, length * 1000 + 1000)
  }, [])

  useEffect(() => {
    if (testType === 'memory') {
      generateSequence(3 + currentQuestion)
    }
  }, [testType, currentQuestion, generateSequence])

  const checkAnswer = (answer: number) => {
    const newInput = [...userInput, answer]
    setUserInput(newInput)

    if (newInput.length === sequence.length) {
      const correct = newInput.every((val, idx) => val === sequence[idx])
      if (correct) {
        setScore(score + 1)
        setFeedback('correct')
      } else {
        setFeedback('wrong')
      }

      setTimeout(() => {
        setFeedback(null)
        if (currentQuestion < 4) {
          setCurrentQuestion(currentQuestion + 1)
        } else {
          onComplete({
            testType: 'Memory Test',
            score: score + (correct ? 1 : 0),
            maxScore: 5,
            timeSpent: Date.now() - startTime,
            details: [
              `Remembered ${score + (correct ? 1 : 0)} out of 5 sequences correctly`,
              `Longest sequence: ${3 + (score + (correct ? 1 : 0))} digits`,
              'Working memory assessment complete'
            ]
          })
        }
      }, 1000)
    }
  }

  // Word Recall for Language Test
  const words = ['APPLE', 'SUNSET', 'GARDEN', 'MOUNTAIN', 'OCEAN']
  const [currentWord, setCurrentWord] = useState('')
  const [wordInput, setWordInput] = useState('')
  const [wordPhase, setWordPhase] = useState<'show' | 'recall'>('show')

  useEffect(() => {
    if (testType === 'language' && currentQuestion < words.length) {
      setCurrentWord(words[currentQuestion])
      setWordPhase('show')
      setWordInput('')

      setTimeout(() => {
        setWordPhase('recall')
      }, 2000)
    }
  }, [testType, currentQuestion])

  const checkWord = () => {
    const correct = wordInput.toUpperCase() === currentWord
    if (correct) setScore(score + 1)
    setFeedback(correct ? 'correct' : 'wrong')

    setTimeout(() => {
      setFeedback(null)
      if (currentQuestion < 4) {
        setCurrentQuestion(currentQuestion + 1)
      } else {
        onComplete({
          testType: 'Language Test',
          score: score + (correct ? 1 : 0),
          maxScore: 5,
          timeSpent: Date.now() - startTime,
          details: [
            `Recalled ${score + (correct ? 1 : 0)} out of 5 words correctly`,
            'Word recognition and recall tested',
            'Verbal memory assessment complete'
          ]
        })
      }
    }, 1000)
  }

  // Attention Test: Find the odd one
  const [attentionGrid, setAttentionGrid] = useState<string[]>([])
  const [oddIndex, setOddIndex] = useState(0)

  useEffect(() => {
    if (testType === 'attention') {
      const symbols = ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
      const odd = Math.floor(Math.random() * 9)
      symbols[odd] = 'Q'
      setAttentionGrid(symbols)
      setOddIndex(odd)
    }
  }, [testType, currentQuestion])

  const checkAttention = (index: number) => {
    const correct = index === oddIndex
    if (correct) setScore(score + 1)
    setFeedback(correct ? 'correct' : 'wrong')

    setTimeout(() => {
      setFeedback(null)
      if (currentQuestion < 4) {
        setCurrentQuestion(currentQuestion + 1)
      } else {
        onComplete({
          testType: 'Attention Test',
          score: score + (correct ? 1 : 0),
          maxScore: 5,
          timeSpent: Date.now() - startTime,
          details: [
            `Found ${score + (correct ? 1 : 0)} out of 5 odd symbols`,
            'Visual attention and focus tested',
            'Selective attention assessment complete'
          ]
        })
      }
    }, 500)
  }

  // Spatial Test: Rotate the shape
  const shapes = ['▲', '►', '▼', '◄']
  const [targetShape, setTargetShape] = useState(0)
  const [currentRotation, setCurrentRotation] = useState(0)

  useEffect(() => {
    if (testType === 'spatial') {
      const target = Math.floor(Math.random() * 4)
      const start = (target + 1 + Math.floor(Math.random() * 3)) % 4
      setTargetShape(target)
      setCurrentRotation(start)
    }
  }, [testType, currentQuestion])

  const rotateShape = (direction: 'left' | 'right') => {
    const newRotation = direction === 'right'
      ? (currentRotation + 1) % 4
      : (currentRotation + 3) % 4
    setCurrentRotation(newRotation)
  }

  const checkSpatial = () => {
    const correct = currentRotation === targetShape
    if (correct) setScore(score + 1)
    setFeedback(correct ? 'correct' : 'wrong')

    setTimeout(() => {
      setFeedback(null)
      if (currentQuestion < 4) {
        setCurrentQuestion(currentQuestion + 1)
      } else {
        onComplete({
          testType: 'Spatial Reasoning',
          score: score + (correct ? 1 : 0),
          maxScore: 5,
          timeSpent: Date.now() - startTime,
          details: [
            `Correctly rotated ${score + (correct ? 1 : 0)} out of 5 shapes`,
            'Mental rotation ability tested',
            'Visual-spatial processing assessment complete'
          ]
        })
      }
    }, 1000)
  }

  // Executive Function: Pattern completion
  const patterns = [
    { sequence: [2, 4, 6, 8], answer: 10 },
    { sequence: [1, 3, 6, 10], answer: 15 },
    { sequence: [3, 6, 12, 24], answer: 48 },
    { sequence: [1, 1, 2, 3, 5], answer: 8 },
    { sequence: [100, 50, 25], answer: 12.5 }
  ]
  const [patternAnswer, setPatternAnswer] = useState('')

  const checkPattern = () => {
    const correct = parseFloat(patternAnswer) === patterns[currentQuestion].answer
    if (correct) setScore(score + 1)
    setFeedback(correct ? 'correct' : 'wrong')

    setTimeout(() => {
      setFeedback(null)
      setPatternAnswer('')
      if (currentQuestion < 4) {
        setCurrentQuestion(currentQuestion + 1)
      } else {
        onComplete({
          testType: 'Executive Function',
          score: score + (correct ? 1 : 0),
          maxScore: 5,
          timeSpent: Date.now() - startTime,
          details: [
            `Solved ${score + (correct ? 1 : 0)} out of 5 pattern problems`,
            'Pattern recognition and logic tested',
            'Problem-solving assessment complete'
          ]
        })
      }
    }, 1000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 flex items-center justify-center p-4">
      <div className="max-w-lg w-full">
        <div className="bg-white rounded-3xl shadow-2xl p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={onExit}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <div className="text-center">
              <h2 className="font-bold text-gray-800">
                {testType === 'memory' && 'Memory Test'}
                {testType === 'attention' && 'Attention Test'}
                {testType === 'language' && 'Language Test'}
                {testType === 'spatial' && 'Spatial Reasoning'}
                {testType === 'executive' && 'Executive Function'}
              </h2>
              <p className="text-sm text-gray-500">Question {currentQuestion + 1} of 5</p>
            </div>
            <div className="text-purple-600 font-bold">{score}/5</div>
          </div>

          {/* Progress */}
          <div className="h-2 bg-gray-200 rounded-full mb-8">
            <div
              className="h-full bg-purple-600 rounded-full transition-all"
              style={{ width: `${((currentQuestion + 1) / 5) * 100}%` }}
            />
          </div>

          {/* Feedback */}
          {feedback && (
            <div className={`mb-6 p-4 rounded-xl text-center ${feedback === 'correct' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {feedback === 'correct' ? 'Correct!' : 'Incorrect'}
            </div>
          )}

          {/* Test Content */}
          {testType === 'memory' && (
            <div className="text-center">
              {showSequence ? (
                <div>
                  <p className="text-gray-600 mb-6">Remember this sequence:</p>
                  <div className="text-6xl font-bold text-purple-600 tracking-widest mb-6">
                    {sequence.join(' ')}
                  </div>
                </div>
              ) : (
                <div>
                  <p className="text-gray-600 mb-6">Enter the sequence:</p>
                  <div className="text-3xl font-bold text-purple-600 mb-6 h-12">
                    {userInput.join(' ') || '-'}
                  </div>
                  <div className="grid grid-cols-3 gap-3">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
                      <button
                        key={num}
                        onClick={() => checkAnswer(num)}
                        className="p-4 bg-purple-100 rounded-xl text-2xl font-bold text-purple-600 hover:bg-purple-200 transition"
                      >
                        {num}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {testType === 'attention' && (
            <div className="text-center">
              <p className="text-gray-600 mb-6">Find the different symbol:</p>
              <div className="grid grid-cols-3 gap-3">
                {attentionGrid.map((symbol, i) => (
                  <button
                    key={i}
                    onClick={() => checkAttention(i)}
                    className="p-6 bg-purple-100 rounded-xl text-3xl font-bold text-purple-600 hover:bg-purple-200 transition"
                  >
                    {symbol}
                  </button>
                ))}
              </div>
            </div>
          )}

          {testType === 'language' && (
            <div className="text-center">
              {wordPhase === 'show' ? (
                <div>
                  <p className="text-gray-600 mb-6">Remember this word:</p>
                  <div className="text-5xl font-bold text-purple-600 mb-6">
                    {currentWord}
                  </div>
                </div>
              ) : (
                <div>
                  <p className="text-gray-600 mb-6">Type the word you saw:</p>
                  <input
                    type="text"
                    value={wordInput}
                    onChange={(e) => setWordInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && checkWord()}
                    className="w-full px-4 py-3 text-center text-2xl border-2 border-purple-300 rounded-xl focus:border-purple-600 focus:outline-none text-gray-900"
                    autoFocus
                  />
                  <button
                    onClick={checkWord}
                    className="mt-4 w-full py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition"
                  >
                    Submit
                  </button>
                </div>
              )}
            </div>
          )}

          {testType === 'spatial' && (
            <div className="text-center">
              <p className="text-gray-600 mb-4">Rotate to match the target:</p>
              <div className="flex justify-around items-center mb-6">
                <div className="text-center">
                  <p className="text-sm text-gray-500 mb-2">Target</p>
                  <div className="text-6xl text-purple-600">{shapes[targetShape]}</div>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-500 mb-2">Your Shape</p>
                  <div className="text-6xl text-blue-600">{shapes[currentRotation]}</div>
                </div>
              </div>
              <div className="flex gap-4 mb-4">
                <button
                  onClick={() => rotateShape('left')}
                  className="flex-1 py-3 bg-gray-200 rounded-xl font-semibold hover:bg-gray-300 transition"
                >
                  ← Rotate Left
                </button>
                <button
                  onClick={() => rotateShape('right')}
                  className="flex-1 py-3 bg-gray-200 rounded-xl font-semibold hover:bg-gray-300 transition"
                >
                  Rotate Right →
                </button>
              </div>
              <button
                onClick={checkSpatial}
                className="w-full py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition"
              >
                Submit
              </button>
            </div>
          )}

          {testType === 'executive' && (
            <div className="text-center">
              <p className="text-gray-600 mb-4">What comes next in the pattern?</p>
              <div className="text-3xl font-bold text-purple-600 mb-6">
                {patterns[currentQuestion].sequence.join(', ')}, ?
              </div>
              <input
                type="number"
                value={patternAnswer}
                onChange={(e) => setPatternAnswer(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && checkPattern()}
                className="w-full px-4 py-3 text-center text-2xl border-2 border-purple-300 rounded-xl focus:border-purple-600 focus:outline-none text-gray-900"
                placeholder="Enter number"
                autoFocus
              />
              <button
                onClick={checkPattern}
                className="mt-4 w-full py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition"
              >
                Submit
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

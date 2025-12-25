'use client'

import React, { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'

interface VoiceCommand {
  patterns: string[]
  action: () => void
  description: string
}

export default function VoiceNavigation() {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [isSupported, setIsSupported] = useState(false)
  const recognitionRef = useRef<any>(null)
  const router = useRouter()

  useEffect(() => {
    // Check if Speech Recognition is supported
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
      if (SpeechRecognition) {
        setIsSupported(true)
        const recognition = new SpeechRecognition()
        recognition.continuous = true
        recognition.interimResults = true
        recognition.lang = 'en-US'

        recognition.onresult = (event: any) => {
          let finalTranscript = ''
          for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript
            }
          }

          if (finalTranscript) {
            setTranscript(finalTranscript.toLowerCase())
            processCommand(finalTranscript.toLowerCase())
          }
        }

        recognition.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error)
          setIsListening(false)
        }

        recognition.onend = () => {
          if (isListening) {
            recognition.start() // Restart if still supposed to be listening
          }
        }

        recognitionRef.current = recognition
      }
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [])

  const voiceCommands: VoiceCommand[] = [
    {
      patterns: ['go home', 'home page', 'main page'],
      action: () => router.push('/'),
      description: 'Navigate to home page'
    },
    {
      patterns: ['dashboard', 'show dashboard'],
      action: () => router.push('/dashboard'),
      description: 'Navigate to dashboard'
    },
    {
      patterns: ['patients', 'show patients', 'patient list'],
      action: () => router.push('/patients'),
      description: 'Navigate to patients page'
    },
    {
      patterns: ['detection', 'ai detection', 'detect'],
      action: () => router.push('/detection'),
      description: 'Navigate to AI detection page'
    },
    {
      patterns: ['tests', 'cognitive tests', 'take test'],
      action: () => router.push('/cognitive-tests'),
      description: 'Navigate to cognitive tests'
    },
    {
      patterns: ['memory care', 'memories'],
      action: () => router.push('/memory-care'),
      description: 'Navigate to memory care'
    },
    {
      patterns: ['help', 'show help', 'what can i say'],
      action: () => showVoiceHelp(),
      description: 'Show available voice commands'
    },
    {
      patterns: ['scroll up', 'go up'],
      action: () => window.scrollBy({ top: -300, behavior: 'smooth' }),
      description: 'Scroll up'
    },
    {
      patterns: ['scroll down', 'go down'],
      action: () => window.scrollBy({ top: 300, behavior: 'smooth' }),
      description: 'Scroll down'
    },
    {
      patterns: ['scroll to top', 'top of page'],
      action: () => window.scrollTo({ top: 0, behavior: 'smooth' }),
      description: 'Scroll to top of page'
    },
    {
      patterns: ['scroll to bottom', 'bottom of page'],
      action: () => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }),
      description: 'Scroll to bottom of page'
    },
    {
      patterns: ['click', 'select', 'choose'],
      action: () => {
        // Find focused element and click it
        const focused = document.activeElement as HTMLElement
        if (focused && focused.click) {
          focused.click()
        }
      },
      description: 'Click focused element'
    }
  ]

  const processCommand = (text: string) => {
    for (const command of voiceCommands) {
      for (const pattern of command.patterns) {
        if (text.includes(pattern)) {
          command.action()
          setTranscript(`✓ ${command.description}`)
          setTimeout(() => setTranscript(''), 2000)
          return
        }
      }
    }

    setTranscript(`❌ Command not recognized: "${text}"`)
    setTimeout(() => setTranscript(''), 3000)
  }

  const showVoiceHelp = () => {
    const helpText = voiceCommands.map(cmd =>
      `• "${cmd.patterns[0]}" - ${cmd.description}`
    ).join('\n')

    alert(`Available Voice Commands:\n\n${helpText}\n\nTip: Say "Help" anytime to see this list again.`)
  }

  const toggleListening = () => {
    if (!isSupported) {
      alert('Voice navigation is not supported in your browser. Please use Chrome, Edge, or Safari.')
      return
    }

    if (isListening) {
      recognitionRef.current?.stop()
      setIsListening(false)
    } else {
      recognitionRef.current?.start()
      setIsListening(true)
    }
  }

  if (!isSupported) {
    return null
  }

  return (
    <div className="fixed bottom-6 left-6 z-50 no-print">
      {/* Voice Control Button */}
      <button
        onClick={toggleListening}
        className={`w-14 h-14 rounded-full shadow-lg transition flex items-center justify-center ${
          isListening
            ? 'bg-red-600 hover:bg-red-700 animate-pulse'
            : 'bg-green-600 hover:bg-green-700'
        }`}
        aria-label={isListening ? 'Stop voice navigation' : 'Start voice navigation'}
        title={isListening ? 'Listening... Click to stop' : 'Click to enable voice navigation'}
      >
        <svg
          className="w-6 h-6 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
          />
        </svg>
      </button>

      {/* Transcript Display */}
      {transcript && (
        <div className="absolute bottom-16 left-0 bg-white dark:bg-gray-800 px-4 py-2 rounded-lg shadow-lg max-w-xs">
          <p className="text-sm text-gray-800 dark:text-gray-200">{transcript}</p>
        </div>
      )}

      {/* Help Button */}
      {isListening && (
        <button
          onClick={showVoiceHelp}
          className="mt-2 w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg transition flex items-center justify-center"
          aria-label="Show voice commands"
          title="Show available voice commands"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </button>
      )}
    </div>
  )
}

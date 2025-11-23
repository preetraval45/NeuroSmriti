'use client'

import { useState, useEffect, useCallback } from 'react'
import Link from 'next/link'

type GameType = 'matching' | 'sequence' | 'word-recall' | 'puzzle' | null

export default function MemoryGamesPage() {
  const [selectedGame, setSelectedGame] = useState<GameType>(null)
  const [scores, setScores] = useState<Record<string, number>>({})

  const games = [
    {
      id: 'matching' as GameType,
      name: 'Memory Match',
      description: 'Classic card matching game to improve visual memory',
      difficulty: 'Easy',
      icon: '🎴',
      color: 'from-pink-500 to-rose-500'
    },
    {
      id: 'sequence' as GameType,
      name: 'Simon Says',
      description: 'Remember and repeat growing color sequences',
      difficulty: 'Medium',
      icon: '🔴',
      color: 'from-purple-500 to-indigo-500'
    },
    {
      id: 'word-recall' as GameType,
      name: 'Word Memory',
      description: 'Remember lists of words in the correct order',
      difficulty: 'Medium',
      icon: '📝',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 'puzzle' as GameType,
      name: 'Number Puzzle',
      description: 'Solve number puzzles to exercise problem-solving',
      difficulty: 'Hard',
      icon: '🧩',
      color: 'from-green-500 to-emerald-500'
    }
  ]

  const handleGameComplete = (gameId: string, score: number) => {
    setScores({ ...scores, [gameId]: Math.max(scores[gameId] || 0, score) })
    setSelectedGame(null)
  }

  if (selectedGame) {
    switch (selectedGame) {
      case 'matching':
        return <MemoryMatchGame onComplete={(score) => handleGameComplete('matching', score)} onExit={() => setSelectedGame(null)} />
      case 'sequence':
        return <SimonSaysGame onComplete={(score) => handleGameComplete('sequence', score)} onExit={() => setSelectedGame(null)} />
      case 'word-recall':
        return <WordRecallGame onComplete={(score) => handleGameComplete('word-recall', score)} onExit={() => setSelectedGame(null)} />
      case 'puzzle':
        return <NumberPuzzleGame onComplete={(score) => handleGameComplete('puzzle', score)} onExit={() => setSelectedGame(null)} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-purple-600 to-pink-600 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Memory Games</h1>
            <p className="text-xl text-purple-100">
              Fun brain exercises to strengthen your cognitive abilities
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Daily Challenge */}
          <div className="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-2xl p-6 mb-8 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold mb-2">Daily Challenge</h3>
                <p className="text-yellow-100">Complete all 4 games today for a bonus!</p>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold">{Object.keys(scores).length}/4</div>
                <div className="text-sm text-yellow-100">Games Completed</div>
              </div>
            </div>
          </div>

          {/* Games Grid */}
          <div className="grid md:grid-cols-2 gap-6 mb-12">
            {games.map((game) => (
              <button
                key={game.id}
                onClick={() => setSelectedGame(game.id)}
                className="bg-white rounded-2xl shadow-lg overflow-hidden text-left hover:shadow-xl transition transform hover:-translate-y-1"
              >
                <div className={`h-32 bg-gradient-to-r ${game.color} flex items-center justify-center`}>
                  <span className="text-6xl">{game.icon}</span>
                </div>
                <div className="p-6">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-xl font-bold text-gray-800">{game.name}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      game.difficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                      game.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {game.difficulty}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-4">{game.description}</p>
                  {scores[game.id ?? ''] !== undefined && (
                    <div className="flex items-center text-purple-600">
                      <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                      <span className="font-semibold">Best: {scores[game.id ?? '']}</span>
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>

          {/* Benefits Section */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h3 className="text-2xl font-bold mb-6 text-center">Benefits of Memory Games</h3>
            <div className="grid md:grid-cols-3 gap-6">
              {[
                { icon: '🧠', title: 'Improved Memory', desc: 'Regular practice strengthens neural pathways' },
                { icon: '⚡', title: 'Faster Processing', desc: 'Games help speed up cognitive processing' },
                { icon: '🎯', title: 'Better Focus', desc: 'Concentration exercises improve attention span' }
              ].map((benefit, i) => (
                <div key={i} className="text-center">
                  <span className="text-4xl mb-3 block">{benefit.icon}</span>
                  <h4 className="font-bold text-gray-800 mb-2">{benefit.title}</h4>
                  <p className="text-gray-600 text-sm">{benefit.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Memory Match Game
function MemoryMatchGame({ onComplete, onExit }: { onComplete: (score: number) => void, onExit: () => void }) {
  const emojis = ['🍎', '🍊', '🍋', '🍇', '🍓', '🍒', '🥝', '🍑']
  const [cards, setCards] = useState<{ id: number; emoji: string; flipped: boolean; matched: boolean }[]>([])
  const [flippedCards, setFlippedCards] = useState<number[]>([])
  const [moves, setMoves] = useState(0)
  const [matches, setMatches] = useState(0)
  const [gameComplete, setGameComplete] = useState(false)

  useEffect(() => {
    const shuffled = [...emojis, ...emojis]
      .sort(() => Math.random() - 0.5)
      .map((emoji, i) => ({ id: i, emoji, flipped: false, matched: false }))
    setCards(shuffled)
  }, [])

  const flipCard = (id: number) => {
    if (flippedCards.length === 2) return
    if (cards[id].flipped || cards[id].matched) return

    const newCards = [...cards]
    newCards[id].flipped = true
    setCards(newCards)

    const newFlipped = [...flippedCards, id]
    setFlippedCards(newFlipped)

    if (newFlipped.length === 2) {
      setMoves(moves + 1)

      if (cards[newFlipped[0]].emoji === cards[newFlipped[1]].emoji) {
        newCards[newFlipped[0]].matched = true
        newCards[newFlipped[1]].matched = true
        setCards(newCards)
        setMatches(matches + 1)
        setFlippedCards([])

        if (matches + 1 === 8) {
          setGameComplete(true)
          onComplete(Math.max(100 - (moves * 2), 10))
        }
      } else {
        setTimeout(() => {
          const resetCards = [...cards]
          resetCards[newFlipped[0]].flipped = false
          resetCards[newFlipped[1]].flipped = false
          setCards(resetCards)
          setFlippedCards([])
        }, 1000)
      }
    }
  }

  if (gameComplete) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl p-8 text-center max-w-md">
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-3xl font-bold mb-2">Great Job!</h2>
          <p className="text-gray-600 mb-4">You completed the game in {moves} moves!</p>
          <div className="text-4xl font-bold text-purple-600 mb-6">Score: {Math.max(100 - (moves * 2), 10)}</div>
          <div className="flex gap-4">
            <button onClick={onExit} className="flex-1 py-3 border border-purple-600 text-purple-600 rounded-xl font-semibold">
              Back
            </button>
            <button onClick={() => window.location.reload()} className="flex-1 py-3 bg-purple-600 text-white rounded-xl font-semibold">
              Play Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-500 to-rose-600 p-4">
      <div className="container mx-auto max-w-lg">
        <div className="flex items-center justify-between text-white mb-6 pt-4">
          <button onClick={onExit} className="p-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <h2 className="text-xl font-bold">Memory Match</h2>
          <div className="text-right">
            <div className="font-bold">Moves: {moves}</div>
            <div className="text-sm">Matches: {matches}/8</div>
          </div>
        </div>

        <div className="grid grid-cols-4 gap-3">
          {cards.map((card) => (
            <button
              key={card.id}
              onClick={() => flipCard(card.id)}
              className={`aspect-square rounded-xl text-4xl flex items-center justify-center transition-all duration-300 transform ${
                card.flipped || card.matched
                  ? 'bg-white rotate-0'
                  : 'bg-white/20 rotate-180'
              } ${card.matched ? 'opacity-50' : ''}`}
            >
              {(card.flipped || card.matched) && card.emoji}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

// Simon Says Game
function SimonSaysGame({ onComplete, onExit }: { onComplete: (score: number) => void, onExit: () => void }) {
  const colors = ['red', 'blue', 'green', 'yellow']
  const [sequence, setSequence] = useState<string[]>([])
  const [userSequence, setUserSequence] = useState<string[]>([])
  const [isPlaying, setIsPlaying] = useState(false)
  const [activeColor, setActiveColor] = useState<string | null>(null)
  const [level, setLevel] = useState(0)
  const [gameOver, setGameOver] = useState(false)

  const playSequence = useCallback(async (seq: string[]) => {
    setIsPlaying(true)
    for (const color of seq) {
      await new Promise(resolve => setTimeout(resolve, 600))
      setActiveColor(color)
      await new Promise(resolve => setTimeout(resolve, 400))
      setActiveColor(null)
    }
    setIsPlaying(false)
  }, [])

  const startNewRound = useCallback(() => {
    const newColor = colors[Math.floor(Math.random() * 4)]
    const newSequence = [...sequence, newColor]
    setSequence(newSequence)
    setUserSequence([])
    setLevel(level + 1)
    playSequence(newSequence)
  }, [sequence, level, playSequence])

  useEffect(() => {
    if (sequence.length === 0) {
      startNewRound()
    }
  }, [])

  const handleColorClick = (color: string) => {
    if (isPlaying) return

    setActiveColor(color)
    setTimeout(() => setActiveColor(null), 200)

    const newUserSequence = [...userSequence, color]
    setUserSequence(newUserSequence)

    const index = newUserSequence.length - 1
    if (newUserSequence[index] !== sequence[index]) {
      setGameOver(true)
      onComplete(level * 10)
      return
    }

    if (newUserSequence.length === sequence.length) {
      setTimeout(startNewRound, 1000)
    }
  }

  if (gameOver) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-700 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl p-8 text-center max-w-md">
          <div className="text-6xl mb-4">🎮</div>
          <h2 className="text-3xl font-bold mb-2">Game Over!</h2>
          <p className="text-gray-600 mb-4">You reached level {level}!</p>
          <div className="text-4xl font-bold text-purple-600 mb-6">Score: {level * 10}</div>
          <div className="flex gap-4">
            <button onClick={onExit} className="flex-1 py-3 border border-purple-600 text-purple-600 rounded-xl font-semibold">
              Back
            </button>
            <button onClick={() => window.location.reload()} className="flex-1 py-3 bg-purple-600 text-white rounded-xl font-semibold">
              Play Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-700 p-4">
      <div className="container mx-auto max-w-md">
        <div className="flex items-center justify-between text-white mb-6 pt-4">
          <button onClick={onExit} className="p-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <h2 className="text-xl font-bold">Simon Says</h2>
          <div className="font-bold">Level {level}</div>
        </div>

        <div className="text-center text-white mb-6">
          {isPlaying ? 'Watch the sequence...' : 'Your turn!'}
        </div>

        <div className="grid grid-cols-2 gap-4 max-w-xs mx-auto">
          {colors.map((color) => (
            <button
              key={color}
              onClick={() => handleColorClick(color)}
              disabled={isPlaying}
              className={`aspect-square rounded-2xl transition-all ${
                activeColor === color ? 'scale-95 brightness-150' : ''
              } ${
                color === 'red' ? 'bg-red-500' :
                color === 'blue' ? 'bg-blue-500' :
                color === 'green' ? 'bg-green-500' :
                'bg-yellow-500'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

// Word Recall Game
function WordRecallGame({ onComplete, onExit }: { onComplete: (score: number) => void, onExit: () => void }) {
  const wordLists = [
    ['CAT', 'DOG', 'BIRD'],
    ['APPLE', 'BANANA', 'ORANGE', 'GRAPE'],
    ['CHAIR', 'TABLE', 'LAMP', 'SOFA', 'BED'],
    ['HAPPY', 'SAD', 'ANGRY', 'CALM', 'EXCITED', 'TIRED']
  ]

  const [level, setLevel] = useState(0)
  const [phase, setPhase] = useState<'show' | 'recall' | 'result'>('show')
  const [currentWords, setCurrentWords] = useState<string[]>([])
  const [userInput, setUserInput] = useState('')
  const [userWords, setUserWords] = useState<string[]>([])
  const [score, setScore] = useState(0)
  const [showingIndex, setShowingIndex] = useState(0)

  useEffect(() => {
    if (level < wordLists.length) {
      setCurrentWords(wordLists[level])
      setPhase('show')
      setShowingIndex(0)
      setUserWords([])
      setUserInput('')
    }
  }, [level])

  useEffect(() => {
    if (phase === 'show' && showingIndex < currentWords.length) {
      const timer = setTimeout(() => {
        setShowingIndex(showingIndex + 1)
      }, 1500)
      return () => clearTimeout(timer)
    } else if (phase === 'show' && showingIndex >= currentWords.length) {
      setTimeout(() => setPhase('recall'), 500)
    }
  }, [phase, showingIndex, currentWords.length])

  const addWord = () => {
    if (userInput.trim()) {
      setUserWords([...userWords, userInput.toUpperCase()])
      setUserInput('')
    }
  }

  const checkAnswers = () => {
    const correct = userWords.filter(word => currentWords.includes(word)).length
    setScore(score + correct * 10)
    setPhase('result')
  }

  const nextLevel = () => {
    if (level < wordLists.length - 1) {
      setLevel(level + 1)
    } else {
      onComplete(score)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-cyan-600 p-4">
      <div className="container mx-auto max-w-md">
        <div className="flex items-center justify-between text-white mb-6 pt-4">
          <button onClick={onExit} className="p-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <h2 className="text-xl font-bold">Word Memory</h2>
          <div className="font-bold">Level {level + 1}</div>
        </div>

        <div className="bg-white rounded-3xl p-6">
          {phase === 'show' && (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-6">Remember these words:</p>
              <div className="text-5xl font-bold text-purple-600 h-16">
                {currentWords[showingIndex] || ''}
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Word {showingIndex + 1} of {currentWords.length}
              </p>
            </div>
          )}

          {phase === 'recall' && (
            <div className="text-center">
              <p className="text-gray-600 mb-4">Type the words you remember:</p>
              <div className="flex gap-2 mb-4">
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addWord()}
                  className="flex-1 px-4 py-3 border-2 border-purple-300 rounded-xl text-gray-900"
                  placeholder="Type a word"
                />
                <button onClick={addWord} className="px-4 py-3 bg-purple-600 text-white rounded-xl">
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2 mb-6">
                {userWords.map((word, i) => (
                  <span key={i} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full">
                    {word}
                  </span>
                ))}
              </div>
              <button
                onClick={checkAnswers}
                className="w-full py-3 bg-purple-600 text-white rounded-xl font-semibold"
              >
                Check Answers
              </button>
            </div>
          )}

          {phase === 'result' && (
            <div className="text-center">
              <p className="text-gray-600 mb-4">Results:</p>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-500">Correct Words</p>
                  <div className="flex flex-wrap gap-1">
                    {currentWords.map((word, i) => (
                      <span key={i} className={`px-2 py-1 rounded text-sm ${
                        userWords.includes(word) ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                      }`}>
                        {word}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Your Score</p>
                  <p className="text-3xl font-bold text-purple-600">{score}</p>
                </div>
              </div>
              <button
                onClick={nextLevel}
                className="w-full py-3 bg-purple-600 text-white rounded-xl font-semibold"
              >
                {level < wordLists.length - 1 ? 'Next Level' : 'Finish'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// Number Puzzle Game
function NumberPuzzleGame({ onComplete, onExit }: { onComplete: (score: number) => void, onExit: () => void }) {
  const [tiles, setTiles] = useState<(number | null)[]>([])
  const [moves, setMoves] = useState(0)
  const [solved, setSolved] = useState(false)

  useEffect(() => {
    // Create shuffled puzzle
    const numbers = [1, 2, 3, 4, 5, 6, 7, 8, null]
    const shuffled = [...numbers].sort(() => Math.random() - 0.5)
    setTiles(shuffled)
  }, [])

  const moveTile = (index: number) => {
    const emptyIndex = tiles.indexOf(null)
    const validMoves = [
      emptyIndex - 1,
      emptyIndex + 1,
      emptyIndex - 3,
      emptyIndex + 3
    ].filter(i => {
      if (i < 0 || i > 8) return false
      if (Math.abs(emptyIndex % 3 - i % 3) > 1) return false
      return true
    })

    if (validMoves.includes(index)) {
      const newTiles = [...tiles]
      newTiles[emptyIndex] = newTiles[index]
      newTiles[index] = null
      setTiles(newTiles)
      setMoves(moves + 1)

      // Check if solved
      const isSolved = newTiles.every((tile, i) =>
        i === 8 ? tile === null : tile === i + 1
      )
      if (isSolved) {
        setSolved(true)
        onComplete(Math.max(100 - moves, 10))
      }
    }
  }

  if (solved) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl p-8 text-center max-w-md">
          <div className="text-6xl mb-4">🏆</div>
          <h2 className="text-3xl font-bold mb-2">Puzzle Solved!</h2>
          <p className="text-gray-600 mb-4">Completed in {moves} moves!</p>
          <div className="text-4xl font-bold text-purple-600 mb-6">Score: {Math.max(100 - moves, 10)}</div>
          <div className="flex gap-4">
            <button onClick={onExit} className="flex-1 py-3 border border-purple-600 text-purple-600 rounded-xl font-semibold">
              Back
            </button>
            <button onClick={() => window.location.reload()} className="flex-1 py-3 bg-purple-600 text-white rounded-xl font-semibold">
              Play Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 to-emerald-600 p-4">
      <div className="container mx-auto max-w-md">
        <div className="flex items-center justify-between text-white mb-6 pt-4">
          <button onClick={onExit} className="p-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <h2 className="text-xl font-bold">Number Puzzle</h2>
          <div className="font-bold">Moves: {moves}</div>
        </div>

        <div className="text-center text-white mb-4">
          Arrange numbers 1-8 in order
        </div>

        <div className="grid grid-cols-3 gap-2 max-w-xs mx-auto">
          {tiles.map((tile, index) => (
            <button
              key={index}
              onClick={() => moveTile(index)}
              className={`aspect-square rounded-xl text-3xl font-bold flex items-center justify-center transition-all ${
                tile ? 'bg-white text-purple-600 hover:scale-95' : 'bg-transparent'
              }`}
            >
              {tile}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

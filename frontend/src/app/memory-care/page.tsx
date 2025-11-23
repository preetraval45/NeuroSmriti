'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function MemoryCarePage() {
  const [selectedMemory, setSelectedMemory] = useState<any>(null)

  const memoryExercises = [
    {
      id: 'spaced-repetition',
      name: 'Spaced Repetition',
      description: 'Review important memories at optimal intervals to strengthen recall',
      icon: '🔄',
      color: 'purple',
      difficulty: 'All Levels'
    },
    {
      id: 'photo-stories',
      name: 'Photo Stories',
      description: 'Connect photos with stories and emotions to create lasting memories',
      icon: '📸',
      color: 'blue',
      difficulty: 'Easy'
    },
    {
      id: 'music-therapy',
      name: 'Music Therapy',
      description: 'Use familiar songs to trigger memories and emotional connections',
      icon: '🎵',
      color: 'pink',
      difficulty: 'Easy'
    },
    {
      id: 'word-games',
      name: 'Word Association',
      description: 'Strengthen language skills and memory connections through word games',
      icon: '💬',
      color: 'green',
      difficulty: 'Medium'
    },
    {
      id: 'puzzle-solving',
      name: 'Puzzle Solving',
      description: 'Exercise problem-solving skills with adaptive difficulty puzzles',
      icon: '🧩',
      color: 'orange',
      difficulty: 'Adaptive'
    },
    {
      id: 'face-recognition',
      name: 'Face & Name Practice',
      description: 'Practice recognizing and naming family members and friends',
      icon: '👥',
      color: 'cyan',
      difficulty: 'Medium'
    }
  ]

  const memories = [
    {
      id: 1,
      type: 'person',
      name: 'Sarah (Daughter)',
      image: '/placeholder-person.jpg',
      strength: 85,
      lastReviewed: '2 days ago',
      details: 'Born 1985, Lives in Boston, Works as a teacher, Has 2 children'
    },
    {
      id: 2,
      type: 'person',
      name: 'Michael (Son)',
      image: '/placeholder-person.jpg',
      strength: 72,
      lastReviewed: '5 days ago',
      details: 'Born 1988, Lives in Chicago, Works as an engineer'
    },
    {
      id: 3,
      type: 'event',
      name: 'Wedding Anniversary',
      image: '/placeholder-event.jpg',
      strength: 90,
      lastReviewed: '1 day ago',
      details: 'Married on June 15, 1975, at St. Mary\'s Church'
    },
    {
      id: 4,
      type: 'place',
      name: 'Childhood Home',
      image: '/placeholder-place.jpg',
      strength: 65,
      lastReviewed: '1 week ago',
      details: '123 Oak Street, Springfield, IL. Lived there 1950-1968'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-pink-600 to-purple-700 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Memory Care Center</h1>
            <p className="text-xl text-pink-100">
              Preserve and strengthen precious memories with AI-powered exercises and tools
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          {/* Memory Bank */}
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Memory Bank</h2>
              <button type="button" className="px-6 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition">
                + Add Memory
              </button>
            </div>

            <div className="grid md:grid-cols-4 gap-6">
              {memories.map(memory => (
                <div
                  key={memory.id}
                  onClick={() => setSelectedMemory(memory)}
                  className="bg-white rounded-2xl shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition transform hover:-translate-y-1"
                >
                  <div className="h-32 bg-gradient-to-br from-purple-200 to-blue-200 flex items-center justify-center">
                    <span className="text-5xl">
                      {memory.type === 'person' ? '👤' : memory.type === 'event' ? '🎉' : '🏠'}
                    </span>
                  </div>
                  <div className="p-4">
                    <h3 className="font-bold mb-1">{memory.name}</h3>
                    <p className="text-sm text-gray-500 mb-3">Last reviewed: {memory.lastReviewed}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-500">Memory Strength</span>
                      <span className={`text-sm font-bold ${
                        memory.strength >= 80 ? 'text-green-600' :
                        memory.strength >= 60 ? 'text-yellow-600' : 'text-red-600'
                      }`}>{memory.strength}%</span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full mt-1 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          memory.strength >= 80 ? 'bg-green-500' :
                          memory.strength >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${memory.strength}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Memory Exercises */}
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Memory Exercises</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {memoryExercises.map(exercise => (
                <div
                  key={exercise.id}
                  className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition cursor-pointer group"
                >
                  <div className={`w-14 h-14 bg-${exercise.color}-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition`}>
                    <span className="text-3xl">{exercise.icon}</span>
                  </div>
                  <h3 className="text-xl font-bold mb-2">{exercise.name}</h3>
                  <p className="text-gray-600 mb-4">{exercise.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">{exercise.difficulty}</span>
                    <button type="button" className={`px-4 py-2 bg-${exercise.color}-600 text-white rounded-lg text-sm font-semibold hover:opacity-90 transition`}>
                      Start
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Daily Memory Goals */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-6">Today&apos;s Memory Goals</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-green-50 rounded-xl">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">✅</span>
                    <span>Review 3 family member memories</span>
                  </div>
                  <span className="text-green-600 font-semibold">Completed</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-xl">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">🔄</span>
                    <span>Complete word association game</span>
                  </div>
                  <span className="text-yellow-600 font-semibold">In Progress</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">⏳</span>
                    <span>Listen to music therapy session</span>
                  </div>
                  <span className="text-gray-500 font-semibold">Pending</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">⏳</span>
                    <span>Add a new memory to your bank</span>
                  </div>
                  <span className="text-gray-500 font-semibold">Pending</span>
                </div>
              </div>
              <div className="mt-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold">Daily Progress</span>
                  <span className="text-purple-600 font-bold">2/4 Complete</span>
                </div>
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full" style={{ width: '50%' }} />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-6">Memory Insights</h2>
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600">Overall Memory Strength</p>
                    <p className="text-3xl font-bold text-purple-600">78%</p>
                  </div>
                  <div className="text-green-500 flex items-center">
                    <span className="text-2xl mr-1">↑</span>
                    <span>+3% this week</span>
                  </div>
                </div>

                <div>
                  <p className="text-gray-600 mb-2">Memories Needing Review</p>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                      <span>Childhood Home</span>
                      <span className="text-red-600 text-sm">Overdue by 3 days</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                      <span>Michael (Son)</span>
                      <span className="text-yellow-600 text-sm">Due tomorrow</span>
                    </div>
                  </div>
                </div>

                <div>
                  <p className="text-gray-600 mb-2">Strongest Memories</p>
                  <div className="flex items-center space-x-2">
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">Wedding Anniversary</span>
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">Sarah (Daughter)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Memory Timeline */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Memory Timeline</h2>
            <p className="text-gray-600 mb-6">A visual journey through your preserved memories</p>

            <div className="relative">
              <div className="absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-purple-200" />

              {[
                { year: '2020', event: 'Grandchild Emma Born', type: 'family' },
                { year: '2015', event: 'Retirement Party', type: 'event' },
                { year: '2000', event: 'Silver Wedding Anniversary', type: 'event' },
                { year: '1985', event: 'Daughter Sarah Born', type: 'family' },
                { year: '1975', event: 'Wedding Day', type: 'event' }
              ].map((item, i) => (
                <div key={i} className={`relative flex items-center mb-8 ${i % 2 === 0 ? 'flex-row-reverse' : ''}`}>
                  <div className={`w-1/2 ${i % 2 === 0 ? 'text-right pr-8' : 'pl-8'}`}>
                    <div className="bg-purple-50 rounded-xl p-4 inline-block">
                      <span className="text-purple-600 font-bold">{item.year}</span>
                      <p className="font-semibold">{item.event}</p>
                    </div>
                  </div>
                  <div className="absolute left-1/2 transform -translate-x-1/2 w-4 h-4 bg-purple-500 rounded-full border-4 border-white" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Memory Detail Modal */}
      {selectedMemory && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">{selectedMemory.name}</h2>
              <button
                type="button"
                onClick={() => setSelectedMemory(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="h-48 bg-gradient-to-br from-purple-200 to-blue-200 rounded-xl flex items-center justify-center mb-6">
              <span className="text-6xl">
                {selectedMemory.type === 'person' ? '👤' : selectedMemory.type === 'event' ? '🎉' : '🏠'}
              </span>
            </div>

            <p className="text-gray-700 mb-6">{selectedMemory.details}</p>

            <div className="flex gap-4">
              <button type="button" className="flex-1 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition">
                Review Memory
              </button>
              <button type="button" className="flex-1 py-3 border-2 border-purple-600 text-purple-600 rounded-xl font-semibold hover:bg-purple-50 transition">
                Edit Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

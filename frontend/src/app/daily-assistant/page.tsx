'use client'

import { useState } from 'react'

export default function DailyAssistantPage() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! I'm your NeuroSmriti AI assistant. I'm here to help you with daily tasks, reminders, and memory support. How can I help you today?" }
  ])
  const [inputValue, setInputValue] = useState('')

  const quickActions = [
    { icon: '💊', label: 'Medication Reminder', action: 'What medications do I need to take today?' },
    { icon: '📅', label: 'Today\'s Schedule', action: 'What\'s on my schedule for today?' },
    { icon: '👥', label: 'Family Info', action: 'Tell me about my family members' },
    { icon: '🏠', label: 'Home Navigation', action: 'Help me find things around the house' },
    { icon: '📞', label: 'Call Someone', action: 'I want to call a family member' },
    { icon: '🧠', label: 'Memory Exercise', action: 'Start a memory exercise' }
  ]

  const dailyReminders = [
    { time: '8:00 AM', task: 'Morning medication', status: 'completed', icon: '💊' },
    { time: '9:00 AM', task: 'Breakfast', status: 'completed', icon: '🍳' },
    { time: '10:30 AM', task: 'Memory exercises', status: 'completed', icon: '🧠' },
    { time: '12:00 PM', task: 'Lunch', status: 'current', icon: '🥗' },
    { time: '2:00 PM', task: 'Afternoon walk', status: 'upcoming', icon: '🚶' },
    { time: '3:30 PM', task: 'Video call with Sarah', status: 'upcoming', icon: '📱' },
    { time: '6:00 PM', task: 'Evening medication', status: 'upcoming', icon: '💊' },
    { time: '7:00 PM', task: 'Dinner', status: 'upcoming', icon: '🍽️' },
    { time: '9:00 PM', task: 'Bedtime routine', status: 'upcoming', icon: '😴' }
  ]

  const handleSend = () => {
    if (!inputValue.trim()) return

    setMessages(prev => [...prev, { role: 'user', content: inputValue }])

    // Simulate AI response
    setTimeout(() => {
      let response = "I understand. Let me help you with that."

      if (inputValue.toLowerCase().includes('medication')) {
        response = "You have the following medications scheduled for today:\n\n💊 **Morning (8:00 AM):** Donepezil 10mg - ✅ Taken\n💊 **Evening (6:00 PM):** Memantine 10mg - ⏳ Upcoming\n💊 **Evening (6:00 PM):** Vitamin E 2000 IU - ⏳ Upcoming\n\nWould you like me to set a reminder for your evening medications?"
      } else if (inputValue.toLowerCase().includes('schedule') || inputValue.toLowerCase().includes('today')) {
        response = "Here's what's on your schedule for today:\n\n✅ 8:00 AM - Morning medication (Done)\n✅ 10:30 AM - Memory exercises (Done)\n⏳ 2:00 PM - Afternoon walk\n⏳ 3:30 PM - Video call with Sarah\n⏳ 6:00 PM - Evening medication\n\nWould you like me to remind you before any of these activities?"
      } else if (inputValue.toLowerCase().includes('family')) {
        response = "Here are your family members:\n\n👩 **Sarah Johnson** - Your daughter\n   Lives in Boston, works as a teacher\n   Has 2 children: Emma (5) and Jake (3)\n\n👨 **Michael Johnson** - Your son\n   Lives in Chicago, works as an engineer\n\n👴 **Robert Johnson** - Your husband\n   You've been married for 49 years\n\nWould you like to see photos or call someone?"
      } else if (inputValue.toLowerCase().includes('call')) {
        response = "Who would you like to call?\n\n📞 Sarah (Daughter) - (555) 123-4567\n📞 Michael (Son) - (555) 234-5678\n📞 Dr. Chen (Doctor) - (555) 987-6543\n\nJust say the name and I'll connect you."
      }

      setMessages(prev => [...prev, { role: 'assistant', content: response }])
    }, 1000)

    setInputValue('')
  }

  const handleQuickAction = (action: string) => {
    setInputValue(action)
    setTimeout(() => handleSend(), 100)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-orange-500 to-pink-600 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Daily Life Assistant</h1>
            <p className="text-xl text-orange-100">
              Your AI companion for daily tasks, reminders, and memory support
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Main Chat Area */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
                {/* Chat Messages */}
                <div className="h-96 overflow-y-auto p-6 space-y-4">
                  {messages.map((msg, i) => (
                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[80%] rounded-2xl p-4 ${
                        msg.role === 'user'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {msg.role === 'assistant' && (
                          <div className="flex items-center mb-2">
                            <span className="text-xl mr-2">🤖</span>
                            <span className="font-semibold">NeuroSmriti Assistant</span>
                          </div>
                        )}
                        <p className="whitespace-pre-line">{msg.content}</p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Quick Actions */}
                <div className="border-t border-gray-200 p-4">
                  <p className="text-sm text-gray-500 mb-3">Quick Actions:</p>
                  <div className="flex flex-wrap gap-2">
                    {quickActions.map((action, i) => (
                      <button
                        key={i}
                        type="button"
                        onClick={() => handleQuickAction(action.action)}
                        className="px-4 py-2 bg-gray-100 hover:bg-purple-100 rounded-full text-sm font-medium transition flex items-center"
                      >
                        <span className="mr-2">{action.icon}</span>
                        {action.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Input Area */}
                <div className="border-t border-gray-200 p-4">
                  <div className="flex items-center space-x-4">
                    <button type="button" className="p-3 bg-gray-100 rounded-full hover:bg-gray-200 transition">
                      <span className="text-xl">🎤</span>
                    </button>
                    <input
                      type="text"
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                      placeholder="Type or speak your question..."
                      className="flex-1 px-6 py-3 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    <button
                      type="button"
                      onClick={handleSend}
                      className="p-3 bg-purple-600 text-white rounded-full hover:bg-purple-700 transition"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              {/* Feature Cards */}
              <div className="grid md:grid-cols-3 gap-4 mt-6">
                <div className="bg-white rounded-xl shadow p-6 text-center hover:shadow-lg transition">
                  <span className="text-4xl block mb-3">📍</span>
                  <h3 className="font-bold mb-2">Location Help</h3>
                  <p className="text-sm text-gray-600">Find your way around home or get directions</p>
                </div>
                <div className="bg-white rounded-xl shadow p-6 text-center hover:shadow-lg transition">
                  <span className="text-4xl block mb-3">🔍</span>
                  <h3 className="font-bold mb-2">Find Things</h3>
                  <p className="text-sm text-gray-600">Help locating commonly misplaced items</p>
                </div>
                <div className="bg-white rounded-xl shadow p-6 text-center hover:shadow-lg transition">
                  <span className="text-4xl block mb-3">📖</span>
                  <h3 className="font-bold mb-2">Story Time</h3>
                  <p className="text-sm text-gray-600">Listen to stories or memories from your life</p>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Daily Schedule */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h2 className="text-xl font-bold mb-4">Today&apos;s Schedule</h2>
                <div className="space-y-3">
                  {dailyReminders.map((reminder, i) => (
                    <div
                      key={i}
                      className={`flex items-center p-3 rounded-xl ${
                        reminder.status === 'completed' ? 'bg-green-50' :
                        reminder.status === 'current' ? 'bg-yellow-50 border-2 border-yellow-300' :
                        'bg-gray-50'
                      }`}
                    >
                      <span className="text-2xl mr-3">{reminder.icon}</span>
                      <div className="flex-1">
                        <p className={`font-medium ${reminder.status === 'completed' ? 'text-gray-500 line-through' : ''}`}>
                          {reminder.task}
                        </p>
                        <p className="text-sm text-gray-500">{reminder.time}</p>
                      </div>
                      {reminder.status === 'completed' && <span className="text-green-500">✓</span>}
                      {reminder.status === 'current' && <span className="text-yellow-500 animate-pulse">●</span>}
                    </div>
                  ))}
                </div>
              </div>

              {/* Emergency Button */}
              <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 text-center">
                <h3 className="text-xl font-bold text-red-800 mb-3">Need Help?</h3>
                <button type="button" className="w-full py-4 bg-red-600 text-white rounded-xl font-bold text-lg hover:bg-red-700 transition">
                  🆘 Emergency Call
                </button>
                <p className="text-sm text-red-600 mt-3">Press to call your emergency contact</p>
              </div>

              {/* Weather Widget */}
              <div className="bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm opacity-80">Today&apos;s Weather</p>
                    <p className="text-4xl font-bold">72°F</p>
                    <p className="opacity-80">Partly Cloudy</p>
                  </div>
                  <span className="text-6xl">⛅</span>
                </div>
                <p className="mt-4 text-sm opacity-80">
                  Good weather for your afternoon walk!
                </p>
              </div>

              {/* Mood Check */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold mb-4">How are you feeling?</h3>
                <div className="flex justify-between">
                  {['😊', '😐', '😔', '😰', '😴'].map((emoji, i) => (
                    <button
                      key={i}
                      type="button"
                      className="text-4xl hover:scale-125 transition transform"
                    >
                      {emoji}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

'use client'

import React, { useState } from 'react'
import Link from 'next/link'

interface QuickAction {
  icon: React.ReactNode
  label: string
  href: string
  color: string
}

export default function QuickActions() {
  const [isOpen, setIsOpen] = useState(false)

  const actions: QuickAction[] = [
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
      ),
      label: 'Take Test',
      href: '/cognitive-tests',
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
      label: 'Patients',
      href: '/patients',
      color: 'bg-green-600 hover:bg-green-700'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      label: 'Dashboard',
      href: '/dashboard',
      color: 'bg-purple-600 hover:bg-purple-700'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
      label: 'Detection',
      href: '/detection',
      color: 'bg-orange-600 hover:bg-orange-700'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      ),
      label: 'Memory Care',
      href: '/memory-care',
      color: 'bg-pink-600 hover:bg-pink-700'
    }
  ]

  return (
    <div className="fixed bottom-24 right-6 z-40 no-print">
      {/* Action Buttons */}
      <div
        className={`flex flex-col-reverse gap-3 mb-3 transition-all duration-300 ${
          isOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
        }`}
      >
        {actions.map((action, index) => (
          <Link
            key={action.href}
            href={action.href}
            className={`flex items-center gap-3 px-4 py-3 rounded-full shadow-lg text-white transition transform hover:scale-105 ${action.color}`}
            style={{
              transitionDelay: isOpen ? `${index * 50}ms` : '0ms'
            }}
            onClick={() => setIsOpen(false)}
          >
            <span className="flex-shrink-0">{action.icon}</span>
            <span className="font-medium whitespace-nowrap">{action.label}</span>
          </Link>
        ))}
      </div>

      {/* Main FAB */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-14 h-14 rounded-full shadow-lg transition transform ${
          isOpen
            ? 'bg-gray-600 hover:bg-gray-700 rotate-45'
            : 'bg-indigo-600 hover:bg-indigo-700'
        } flex items-center justify-center text-white`}
        aria-label={isOpen ? 'Close quick actions' : 'Open quick actions'}
        aria-expanded={isOpen}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v16m8-8H4"
          />
        </svg>
      </button>

      {/* Label */}
      {!isOpen && (
        <div className="absolute right-16 top-3 bg-gray-900 text-white px-3 py-1 rounded text-sm whitespace-nowrap opacity-0 hover:opacity-100 transition pointer-events-none">
          Quick Actions
        </div>
      )}
    </div>
  )
}

'use client'

import React, { useState } from 'react'
import { useTheme } from '@/contexts/ThemeContext'
import type { ThemeMode, ColorBlindMode, TextSize, ContrastMode, ComplexityLevel } from '@/contexts/ThemeContext'

export default function AccessibilitySettings() {
  const { settings, updateTheme, resetTheme } = useTheme()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Accessibility Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 transition flex items-center justify-center no-print"
        aria-label="Accessibility Settings"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </button>

      {/* Settings Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto no-print">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            {/* Backdrop */}
            <div
              className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
              onClick={() => setIsOpen(false)}
            ></div>

            {/* Modal Panel */}
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-2xl font-bold text-gray-900">
                    Accessibility Settings
                  </h3>
                  <button
                    onClick={() => setIsOpen(false)}
                    className="text-gray-400 hover:text-gray-500"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                <div className="space-y-6">
                  {/* Theme Mode */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Theme Mode
                    </label>
                    <div className="flex gap-3">
                      <button
                        onClick={() => updateTheme({ mode: 'light' })}
                        className={`flex-1 px-4 py-3 rounded-lg border-2 transition ${
                          settings.mode === 'light'
                            ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                            : 'border-gray-300 hover:border-gray-400'
                        }`}
                      >
                        ☀️ Light
                      </button>
                      <button
                        onClick={() => updateTheme({ mode: 'dark' })}
                        className={`flex-1 px-4 py-3 rounded-lg border-2 transition ${
                          settings.mode === 'dark'
                            ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                            : 'border-gray-300 hover:border-gray-400'
                        }`}
                      >
                        🌙 Dark
                      </button>
                    </div>
                  </div>

                  {/* Text Size */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Text Size
                    </label>
                    <div className="flex gap-3">
                      {(['normal', 'large', 'extra-large'] as TextSize[]).map((size) => (
                        <button
                          key={size}
                          onClick={() => updateTheme({ textSize: size })}
                          className={`flex-1 px-4 py-3 rounded-lg border-2 transition ${
                            settings.textSize === size
                              ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          {size === 'normal' ? 'A' : size === 'large' ? 'A+' : 'A++'}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Contrast Mode */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Contrast
                    </label>
                    <div className="flex gap-3">
                      {(['normal', 'high', 'extra-high'] as ContrastMode[]).map((mode) => (
                        <button
                          key={mode}
                          onClick={() => updateTheme({ contrastMode: mode })}
                          className={`flex-1 px-4 py-3 rounded-lg border-2 transition ${
                            settings.contrastMode === mode
                              ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          {mode === 'normal' ? 'Normal' : mode === 'high' ? 'High' : 'Extra High'}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Color Blind Mode */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Color Blind Mode
                    </label>
                    <select
                      value={settings.colorBlindMode}
                      onChange={(e) => updateTheme({ colorBlindMode: e.target.value as ColorBlindMode })}
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-600 focus:outline-none"
                    >
                      <option value="none">None</option>
                      <option value="protanopia">Protanopia (Red-Blind)</option>
                      <option value="deuteranopia">Deuteranopia (Green-Blind)</option>
                      <option value="tritanopia">Tritanopia (Blue-Blind)</option>
                    </select>
                  </div>

                  {/* Interface Complexity */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Interface Complexity
                    </label>
                    <div className="flex gap-3">
                      {(['full', 'simplified', 'minimal'] as ComplexityLevel[]).map((level) => (
                        <button
                          key={level}
                          onClick={() => updateTheme({ complexityLevel: level })}
                          className={`flex-1 px-4 py-3 rounded-lg border-2 transition ${
                            settings.complexityLevel === level
                              ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          {level === 'full' ? 'Full' : level === 'simplified' ? 'Simple' : 'Minimal'}
                        </button>
                      ))}
                    </div>
                    <p className="mt-2 text-sm text-gray-500">
                      {settings.complexityLevel === 'minimal' && 'Large buttons, essential features only'}
                      {settings.complexityLevel === 'simplified' && 'Larger buttons, fewer options'}
                      {settings.complexityLevel === 'full' && 'All features and options available'}
                    </p>
                  </div>

                  {/* Reduce Motion */}
                  <div>
                    <label className="flex items-center justify-between cursor-pointer">
                      <span className="text-sm font-medium text-gray-700">
                        Reduce Motion
                      </span>
                      <div className="relative">
                        <input
                          type="checkbox"
                          checked={settings.reduceMotion}
                          onChange={(e) => updateTheme({ reduceMotion: e.target.checked })}
                          className="sr-only"
                        />
                        <div
                          onClick={() => updateTheme({ reduceMotion: !settings.reduceMotion })}
                          className={`block w-14 h-8 rounded-full transition ${
                            settings.reduceMotion ? 'bg-indigo-600' : 'bg-gray-300'
                          }`}
                        >
                          <div
                            className={`dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition ${
                              settings.reduceMotion ? 'transform translate-x-6' : ''
                            }`}
                          ></div>
                        </div>
                      </div>
                    </label>
                    <p className="mt-1 text-sm text-gray-500">
                      Minimizes animations and transitions
                    </p>
                  </div>
                </div>
              </div>

              {/* Footer */}
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse gap-3">
                <button
                  onClick={() => setIsOpen(false)}
                  className="w-full sm:w-auto px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                >
                  Done
                </button>
                <button
                  onClick={() => {
                    resetTheme()
                    setIsOpen(false)
                  }}
                  className="w-full sm:w-auto mt-3 sm:mt-0 px-6 py-2 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition"
                >
                  Reset to Default
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

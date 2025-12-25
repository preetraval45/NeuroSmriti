'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'

export type ThemeMode = 'light' | 'dark'
export type ColorBlindMode = 'none' | 'protanopia' | 'deuteranopia' | 'tritanopia'
export type TextSize = 'normal' | 'large' | 'extra-large'
export type ContrastMode = 'normal' | 'high' | 'extra-high'
export type ComplexityLevel = 'full' | 'simplified' | 'minimal'

interface ThemeSettings {
  mode: ThemeMode
  colorBlindMode: ColorBlindMode
  textSize: TextSize
  contrastMode: ContrastMode
  reduceMotion: boolean
  customColors: {
    primary?: string
    secondary?: string
    background?: string
  }
  complexityLevel: ComplexityLevel
}

interface ThemeContextType {
  settings: ThemeSettings
  updateTheme: (updates: Partial<ThemeSettings>) => void
  resetTheme: () => void
}

const defaultSettings: ThemeSettings = {
  mode: 'light',
  colorBlindMode: 'none',
  textSize: 'normal',
  contrastMode: 'normal',
  reduceMotion: false,
  customColors: {},
  complexityLevel: 'full'
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [settings, setSettings] = useState<ThemeSettings>(defaultSettings)

  // Load settings from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('neurosmriti-theme')
    if (saved) {
      try {
        setSettings(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to load theme settings:', e)
      }
    }

    // Check system preferences
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setSettings(prev => ({ ...prev, mode: 'dark' }))
    }

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setSettings(prev => ({ ...prev, reduceMotion: true }))
    }
  }, [])

  // Save settings to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('neurosmriti-theme', JSON.stringify(settings))
    applyThemeToDOM(settings)
  }, [settings])

  const updateTheme = (updates: Partial<ThemeSettings>) => {
    setSettings(prev => ({ ...prev, ...updates }))
  }

  const resetTheme = () => {
    setSettings(defaultSettings)
  }

  return (
    <ThemeContext.Provider value={{ settings, updateTheme, resetTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

// Apply theme settings to DOM
function applyThemeToDOM(settings: ThemeSettings) {
  const root = document.documentElement

  // Dark mode
  if (settings.mode === 'dark') {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }

  // Text size
  root.classList.remove('text-normal', 'text-large', 'text-extra-large')
  root.classList.add(`text-${settings.textSize}`)

  // Contrast mode
  root.classList.remove('contrast-normal', 'contrast-high', 'contrast-extra-high')
  root.classList.add(`contrast-${settings.contrastMode}`)

  // Color blind mode
  root.classList.remove('cb-none', 'cb-protanopia', 'cb-deuteranopia', 'cb-tritanopia')
  root.classList.add(`cb-${settings.colorBlindMode}`)

  // Reduce motion
  if (settings.reduceMotion) {
    root.classList.add('reduce-motion')
  } else {
    root.classList.remove('reduce-motion')
  }

  // Complexity level
  root.classList.remove('complexity-full', 'complexity-simplified', 'complexity-minimal')
  root.classList.add(`complexity-${settings.complexityLevel}`)

  // Custom colors
  if (settings.customColors.primary) {
    root.style.setProperty('--color-primary', settings.customColors.primary)
  }
  if (settings.customColors.secondary) {
    root.style.setProperty('--color-secondary', settings.customColors.secondary)
  }
  if (settings.customColors.background) {
    root.style.setProperty('--color-background', settings.customColors.background)
  }
}

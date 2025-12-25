import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import './accessibility.css'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import { ThemeProvider } from '@/contexts/ThemeContext'
import GestureHandler from '@/components/GestureHandler'
import AccessibilitySettings from '@/components/AccessibilitySettings'
import VoiceNavigation from '@/components/VoiceNavigation'
import Breadcrumbs from '@/components/Breadcrumbs'
import QuickActions from '@/components/QuickActions'
import EmergencyPanel from '@/components/EmergencyPanel'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'NeuroSmriti - AI-Powered Alzheimer\'s Detection & Cognitive Care',
  description: 'Revolutionary AI platform for early Alzheimer\'s detection, personalized treatment plans, memory preservation, and comprehensive caregiver support. 94%+ detection accuracy across all stages.',
  keywords: 'Alzheimer\'s detection, cognitive care, AI healthcare, memory preservation, dementia care, caregiver support, brain health',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider>
          <GestureHandler>
            {/* Skip to main content link for keyboard navigation */}
            <a
              href="#main-content"
              className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded"
            >
              Skip to main content
            </a>

            <Navbar />
            <Breadcrumbs />

            <main id="main-content">
              {children}
            </main>

            <Footer />

            {/* Floating UI Components */}
            <AccessibilitySettings />
            <VoiceNavigation />
            <QuickActions />
            <EmergencyPanel />
          </GestureHandler>
        </ThemeProvider>
      </body>
    </html>
  )
}

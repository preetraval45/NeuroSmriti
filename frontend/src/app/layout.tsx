import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

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
        <Navbar />
        <main className="pt-20">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}

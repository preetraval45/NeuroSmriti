'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Logo from './Logo'

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const user = localStorage.getItem('user')
    setIsLoggedIn(!!user)

    const handleScroll = () => {
      setScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setIsLoggedIn(false)
    router.push('/')
  }

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/detection', label: 'AI Detection' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/patients', label: 'Patients' },
    { href: '/cognitive-tests', label: 'Tests' },
    { href: '/memory-care', label: 'Memory Care' },
    { href: '/about', label: 'About' },
    { href: '/contact', label: 'Contact' },
  ]

  return (
    <>
      {/* Top Medical Bar */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 text-white text-xs">
        <div className="w-full px-6 py-1.5">
          <div className="flex justify-between items-center max-w-[1920px] mx-auto">
            <div className="flex items-center gap-6">
              <span className="flex items-center gap-1.5">
                <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                </svg>
                <span className="hidden md:inline">Clinical AI Research Platform</span>
              </span>
              <span className="flex items-center gap-1.5">
                <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                </svg>
                <span className="hidden lg:inline">Research Support: research@neurosmriti.com</span>
              </span>
            </div>
            <div className="flex items-center gap-4">
              <span className="px-2 py-0.5 bg-white/20 rounded text-[10px] font-medium">RESEARCH PROTOTYPE</span>
              <span className="hidden sm:inline text-[10px]">Not for Clinical Use</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className={`fixed top-[26px] left-0 right-0 z-40 transition-all duration-300 ${
        scrolled
          ? 'bg-white shadow-xl border-b-2 border-indigo-100'
          : 'bg-white/95 backdrop-blur-lg shadow-md'
      }`}>
        <div className="w-full px-6">
          <div className="flex justify-between items-center h-20 max-w-[1920px] mx-auto">

            {/* Logo Section - Left */}
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-14 h-14 flex-shrink-0 transform group-hover:scale-105 transition-transform">
                <Logo size={56} />
              </div>
              <div className="flex flex-col">
                <span className="text-2xl lg:text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-700 via-purple-600 to-blue-600">
                  NeuroSmriti
                </span>
                <span className="text-[10px] lg:text-xs text-gray-600 font-medium tracking-wider uppercase">
                  AI-Powered Cognitive Care
                </span>
              </div>
            </Link>

            {/* Center Navigation - Desktop */}
            <div className="hidden xl:flex items-center gap-1">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="px-4 py-2.5 text-sm font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all duration-200"
                >
                  {link.label}
                </Link>
              ))}
            </div>

            {/* Right Side - CTA Buttons */}
            <div className="hidden lg:flex items-center gap-3">
              {isLoggedIn ? (
                <>
                  <button
                    type="button"
                    aria-label="View notifications"
                    className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                    </svg>
                  </button>
                  <button
                    type="button"
                    onClick={handleLogout}
                    className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-indigo-200 transition-all duration-200 text-sm"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    className="px-6 py-2.5 text-indigo-600 font-semibold hover:text-indigo-700 transition-colors text-sm border-2 border-indigo-600 rounded-lg hover:bg-indigo-50"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/register"
                    className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-indigo-200 transition-all duration-200 text-sm"
                  >
                    Get Started
                  </Link>
                </>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              type="button"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="xl:hidden p-2.5 text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
              aria-label="Toggle menu"
            >
              <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className={`xl:hidden overflow-hidden transition-all duration-300 border-t border-indigo-100 ${
          isMenuOpen ? 'max-h-[600px] opacity-100' : 'max-h-0 opacity-0'
        }`}>
          <div className="px-6 py-6 bg-gradient-to-b from-white to-indigo-50/30">
            <div className="flex flex-col gap-2 mb-6">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="px-4 py-3.5 text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-white rounded-xl transition-all duration-200 shadow-sm hover:shadow-md"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
            </div>

            <div className="pt-6 border-t border-indigo-200 space-y-3">
              {isLoggedIn ? (
                <button
                  type="button"
                  onClick={() => { handleLogout(); setIsMenuOpen(false); }}
                  className="w-full px-6 py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all"
                >
                  Logout
                </button>
              ) : (
                <>
                  <Link
                    href="/login"
                    className="block px-6 py-3.5 text-center text-indigo-600 font-semibold border-2 border-indigo-600 rounded-xl hover:bg-indigo-50 transition-all"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/register"
                    className="block px-6 py-3.5 text-center bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Spacer to prevent content from going under fixed navbar */}
      <div className="h-[106px]"></div>
    </>
  )
}
